# Loyalty Platform Database Setup Guide

## Database Overview
The Loyalty Platform uses MySQL 8.0 running on dedicated on-premises servers with master-slave replication for high availability.

## Environment Details

### Development Database
- **Host**: loyalty-dev-mysql.optum.com
- **Port**: 3306
- **Database**: loyalty_platform_dev
- **Username**: loyalty_dev_user
- **Connection Pool**: 20 connections max

### Stage Database
- **Host**: loyalty-stage-mysql.optum.com  
- **Port**: 3306
- **Database**: loyalty_platform_stage
- **Username**: loyalty_stage_user
- **Connection Pool**: 30 connections max

### Production Database
- **Host**: loyalty-prod-mysql.optum.com
- **Port**: 3306  
- **Database**: loyalty_platform_prod
- **Username**: loyalty_prod_user
- **Connection Pool**: 50 connections max
- **Read Replica**: loyalty-prod-mysql-read.optum.com

## Schema Setup

### Core Tables
```sql
-- Member management table
CREATE TABLE loyalty_members (
    member_id VARCHAR(36) PRIMARY KEY,
    uhc_member_id VARCHAR(20) NOT NULL UNIQUE,
    partner VARCHAR(50) NOT NULL,
    client VARCHAR(100),
    affiliation VARCHAR(100) NOT NULL,
    enrollment_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    family_id VARCHAR(36),
    spouse_assignment_status VARCHAR(20) DEFAULT 'PENDING',
    spouse_assignment_date TIMESTAMP NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_uhc_member_id (uhc_member_id),
    INDEX idx_family_id (family_id),
    INDEX idx_partner_client (partner, client),
    INDEX idx_status_enrollment (status, enrollment_date)
);

-- Member eligibility tracking
CREATE TABLE member_eligibilities (
    eligibility_id VARCHAR(36) PRIMARY KEY,
    member_id VARCHAR(36) NOT NULL,
    eligibility_type VARCHAR(50) NOT NULL,
    plan_code VARCHAR(20),
    effective_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    processing_source VARCHAR(50) DEFAULT 'KAFKA',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (member_id) REFERENCES loyalty_members(member_id),
    INDEX idx_member_status (member_id, status),
    INDEX idx_effective_dates (effective_date, end_date),
    INDEX idx_plan_code (plan_code)
);
```

## Common Database Operations

### Member Lookup Queries
```sql
-- Find member by UHC ID
SELECT m.*, fm.relationship_type, fm.primary_member 
FROM loyalty_members m
LEFT JOIN family_members fm ON m.member_id = fm.member_id
WHERE m.uhc_member_id = 'UHC12345001';

-- Check for dual eligibility
SELECT m.member_id, m.uhc_member_id, COUNT(me.eligibility_id) as active_eligibilities
FROM loyalty_members m
JOIN member_eligibilities me ON m.member_id = me.member_id
WHERE me.status = 'ACTIVE'
GROUP BY m.member_id, m.uhc_member_id
HAVING active_eligibilities > 1;
```

### Troubleshooting Queries
```sql
-- Members with spouse assignment issues
SELECT member_id, uhc_member_id, spouse_assignment_status, enrollment_date
FROM loyalty_members 
WHERE spouse_assignment_status = 'FAILED'
AND enrollment_date > DATE_SUB(NOW(), INTERVAL 7 DAY);

-- Recent eligibility processing errors
SELECT member_id, processing_type, processing_status, error_details, processing_timestamp
FROM eligibility_processing_log
WHERE processing_status = 'ERROR'
AND processing_timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY)
ORDER BY processing_timestamp DESC;
```

## Database Maintenance

### Daily Health Checks
```sql
-- Check connection pool usage
SHOW PROCESSLIST;

-- Monitor slow queries
SELECT * FROM information_schema.processlist 
WHERE command != 'Sleep' AND time > 30;

-- Check table sizes
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'loyalty_platform_prod'
ORDER BY (data_length + index_length) DESC;
```