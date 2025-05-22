#!/usr/bin/env python3
"""
Script to create realistic Optum Loyalty team documents for demo
Run this script to generate all the sample documents
"""

import os
import shutil

def create_optum_docs():
    # Remove existing docs folder if it exists
    if os.path.exists('docs'):
        print("🗑️  Removing existing docs folder...")
        shutil.rmtree('docs')
    
    # Create fresh docs directory
    os.makedirs('docs', exist_ok=True)
    print("📁 Created docs directory")
    
    # Document contents
    docs = {
        'docs/README.md': '''# Optum Loyalty Platform

## Overview
The Optum Loyalty Platform rewards UnitedHealthcare and Optum members for healthy behaviors including preventive care visits, fitness activities, and wellness program participation. Our backend services process member eligibility, track activities, and manage point awards.

## Architecture Overview
The Loyalty platform consists of multiple microservices deployed on Kubernetes:

### Core Services
- **Loyalty-Member**: Tracks member details, partner/client affiliations, and eligibility status
- **Loyalty-Eligibility**: Manages member eligibility rules and enrollment verification  
- **Loyalty-Services**: Handles Electronic Device Gateway (EDG) integrations with fitness trackers
- **Loyalty-Points**: Calculates and awards points for qualifying activities
- **Loyalty-Rewards**: Manages reward catalog and redemption processing

### Technology Stack
- **Backend**: Java Spring Boot
- **Database**: MySQL (on-premises)
- **Container Platform**: Kubernetes
- **Messaging**: Apache Kafka
- **Monitoring**: Splunk
- **Frontend Partner**: Capillary Technologies

## Team Structure
### Onshore Teams
- **Taj Mahal Team**: Primary development team
- **Machu Picchu Team**: Feature development and maintenance

### Offshore Teams  
- **Acropolis Team**: Support and maintenance
- **Pyramids Team**: QA and testing support

## Environments
- **Development**: For active development and testing
- **Stage**: Pre-production validation environment
- **Production**: Live member-facing environment''',

        'docs/team_contacts.json': '''{
  "loyalty_organization": {
    "leadership": {
      "director": {
        "name": "Christopher Jimenez",
        "email": "christopher.jimenez@optum.com",
        "role": "Engineering Director - Loyalty Platform"
      },
      "manager": {
        "name": "Allesha Fogle", 
        "email": "allesha.fogle@optum.com",
        "phone": "612-555-0147",
        "role": "Engineering Manager - Onshore Teams",
        "teams_managed": ["Taj Mahal", "Machu Picchu"]
      }
    },
    "product_team": {
      "product_manager": {
        "name": "Connie Cavallo",
        "email": "connie.cavallo@optum.com", 
        "phone": "612-555-0189",
        "role": "Senior Product Manager"
      },
      "scrum_master": {
        "name": "Swapna Kolimi",
        "email": "swapna.kolimi@optum.com",
        "phone": "612-555-0156", 
        "role": "Scrum Master"
      }
    },
    "engineering_teams": {
      "taj_mahal": {
        "focus": "Loyalty-Member service and core platform features",
        "members": [
          {
            "name": "Britney Duratinsky",
            "email": "britney.duratinsky@optum.com",
            "phone": "612-555-0123",
            "role": "Associate Software Engineer"
          },
          {
            "name": "Scott Forsmann", 
            "email": "scott.forsmann@optum.com",
            "phone": "612-555-0134",
            "role": "Associate Software Engineer"
          },
          {
            "name": "Kavya Kali",
            "email": "kavya.kali@optum.com",
            "phone": "612-555-0145",
            "role": "Software Engineer Contractor"
          }
        ]
      },
      "machu_picchu": {
        "focus": "Loyalty-Eligibility and integration services", 
        "members": [
          {
            "name": "Sofia Khan",
            "email": "sofia.khan@optum.com", 
            "phone": "612-555-0167",
            "role": "Associate Software Engineer"
          },
          {
            "name": "Ravali Botta",
            "email": "ravali.botta@optum.com",
            "phone": "612-555-0178", 
            "role": "Software Engineer"
          },
          {
            "name": "Michael Joyce",
            "email": "michael.joyce@optum.com",
            "phone": "612-555-0189",
            "role": "Associate Software Engineer"
          },
          {
            "name": "Shasikumar Bommineni",
            "email": "shasikumar.bommineni@optum.com",
            "phone": "612-555-0190",
            "role": "Software Engineer Contractor"
          },
          {
            "name": "Ganesh Nettem", 
            "email": "ganesh.nettem@optum.com",
            "phone": "612-555-0201",
            "role": "Software Engineer Contractor"
          },
          {
            "name": "Nagarjuna Reddy",
            "email": "nagarjuna.reddy@optum.com",
            "phone": "612-555-0212",
            "role": "Software Engineer"
          },
          {
            "name": "Ajit Krishnan",
            "email": "ajit.krishnan@optum.com", 
            "phone": "612-555-0223",
            "role": "Software Engineer"
          }
        ]
      }
    }
  },
  "on_call_rotation": {
    "current_week": "Scott Forsmann",
    "next_week": "Ravali Botta", 
    "escalation_primary": "Allesha Fogle",
    "escalation_secondary": "Christopher Jimenez"
  },
  "emergency_contacts": {
    "production_incidents": "loyalty-oncall@optum.com",
    "database_issues": "dba-team@optum.com",
    "kubernetes_platform": "platform-team@optum.com",
    "security_incidents": "security@optum.com"
  }
}''',

        'docs/loyalty_member_service.md': '''# Loyalty-Member Service Documentation

## Overview
The Loyalty-Member service is the core service responsible for managing member data, tracking partner/client affiliations, and maintaining member eligibility status within the Optum Loyalty Platform.

## Service Responsibilities
- Member profile management and data integrity
- Partner and client affiliation tracking 
- Member eligibility status coordination
- Family member relationship management
- Member enrollment and lifecycle events

## Key Data Models

### Member Entity
- **member_id**: Unique identifier for the member
- **uhc_member_id**: UnitedHealthcare member identifier
- **partner**: Partner organization (e.g., "UHC", "Optum")
- **client**: Specific client within partner (e.g., plan codes)
- **affiliation**: Member's current affiliation status
- **enrollment_date**: Date member enrolled in loyalty program
- **status**: Active, Inactive, Suspended
- **family_id**: Links family members together

### Common Affiliations
- **UHC_INDIVIDUAL**: Individual UnitedHealthcare member
- **UHC_FAMILY_PRIMARY**: Primary family member for UHC plan
- **UHC_FAMILY_DEPENDENT**: Dependent family member
- **OPTUM_EMPLOYEE**: Optum employee enrollment
- **DUAL_ELIGIBLE**: Members with multiple plan eligibilities

## API Endpoints

### Member Management
```
GET /loyalty-member/v1/members/{memberId}
PUT /loyalty-member/v1/members/{memberId}
POST /loyalty-member/v1/members
DELETE /loyalty-member/v1/members/{memberId}
```

### Affiliation Management
```
GET /loyalty-member/v1/members/{memberId}/affiliations
POST /loyalty-member/v1/members/{memberId}/affiliations
PUT /loyalty-member/v1/affiliations/{affiliationId}
```

### Family Member Operations
```
GET /loyalty-member/v1/families/{familyId}/members
POST /loyalty-member/v1/families/{familyId}/members
DELETE /loyalty-member/v1/families/{familyId}/members/{memberId}
```

## Database Schema
```sql
CREATE TABLE loyalty_members (
    member_id VARCHAR(36) PRIMARY KEY,
    uhc_member_id VARCHAR(20) NOT NULL,
    partner VARCHAR(50) NOT NULL,
    client VARCHAR(100),
    affiliation VARCHAR(100) NOT NULL,
    enrollment_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    family_id VARCHAR(36),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_uhc_member_id (uhc_member_id),
    INDEX idx_family_id (family_id),
    INDEX idx_partner_client (partner, client)
);
```

## Kafka Topics
```
- loyalty.member.created: Member creation events
- loyalty.member.updated: Member update events
- loyalty.member.deleted: Member deletion events
- loyalty.affiliation.changed: Affiliation change events
```

## Error Handling
- All API endpoints return standard HTTP status codes
- Detailed error messages in response body
- Error logging to Splunk for monitoring

## Monitoring
- Service health metrics via Spring Boot Actuator
- Custom metrics for member operations
- Alert thresholds for error rates and latency

## Deployment
- Kubernetes deployment with 3 replicas
- Rolling updates for zero downtime
- Health checks and readiness probes
- Resource limits and requests configured

## Security
- OAuth2 authentication required
- Role-based access control
- Audit logging for all operations
- PII data encryption at rest
''',

        'docs/sprint_23_planning.txt': '''Sprint 23 Planning - Loyalty Platform
Sprint Dates: January 15 - January 29, 2025

SPRINT GOAL: Kafka Migration Phase 1 - Eliminate Top of Funnel Script Dependencies

KEY INITIATIVES:
1. Replace Top of Funnel script with real-time Kafka-based eligibility processing
2. Implement automated spouse assignment workflow
3. Fix dual eligibility conflict resolution
4. Database performance improvements for member lookup queries

USER STORIES - TAJ MAHAL TEAM:
- [LY-1847] As a system, I need to process eligibility updates via Kafka instead of batch scripts
- [LY-1848] As a member, I want my spouse to be automatically assigned to my family membership
- [LY-1849] As a developer, I need improved database query performance for member searches
- [LY-1850] As a system, I need to handle dual eligibility scenarios without manual intervention

USER STORIES - MACHU PICCHU TEAM:  
- [LY-1851] As a member, I want my fitness device data to sync reliably without delays
- [LY-1852] As a system, I need to migrate eligibility rules from Top of Funnel to event-driven processing
- [LY-1853] As a support agent, I need better error messages for eligibility failures
- [LY-1854] As a developer, I need monitoring alerts for Kafka consumer lag

TECHNICAL DEBT:
- Remove deprecated Top of Funnel script dependencies
- Update member eligibility documentation
- Refactor spouse assignment logic for better error handling
- Add comprehensive unit tests for dual eligibility scenarios

DEPENDENCIES:
- Platform team: Kafka topic creation and permissions
- DBA team: Database index optimization review
- Security team: New service-to-service authentication tokens

RISKS:
- Top of Funnel script still needed as fallback during transition
- Dual eligibility logic complexity may cause delays
- Kafka consumer performance under high load needs validation

TEAM CAPACITY:
- Taj Mahal: 42 story points planned, 45 point velocity
- Machu Picchu: 38 story points planned, 40 point velocity

DEFINITION OF DONE:
- All code reviewed and approved
- Unit tests with 80%+ coverage
- Integration tests passing in dev and stage
- Performance tests completed
- Documentation updated
- Deployed to stage environment''',

        'docs/kafka_migration_edr.md': '''# Engineering Design Record (EDR): Kafka-Based Eligibility Processing

**EDR ID**: LY-EDR-2025-003  
**Author**: Taj Mahal Team  
**Date**: January 8, 2025  
**Status**: Approved  

## Problem Statement
The current Top of Funnel script runs daily as a batch process to manually configure member eligibility, creating delays in member enrollment and causing data inconsistencies. This approach doesn't scale with our growing member base and prevents real-time eligibility updates.

## Current State Analysis
### Existing Architecture
- **Top of Funnel Script**: Perl script running daily via cron job
- **Eligibility Database**: MySQL tables updated once per day
- **Manual Interventions**: Support team regularly fixes eligibility conflicts
- **Processing Time**: 4-6 hours for full member base processing
- **Failure Recovery**: Manual restart and data reconciliation required

### Pain Points
1. **Delayed Eligibility**: New members wait up to 24 hours for loyalty program access
2. **Dual Eligibility Issues**: Script cannot handle complex eligibility scenarios
3. **Spouse Assignment Failures**: Manual intervention required for 15% of family enrollments
4. **Poor Observability**: Limited logging and monitoring of eligibility processing
5. **Technical Debt**: Legacy Perl codebase with minimal documentation

## Proposed Solution

### High-Level Architecture
Replace batch processing with event-driven Kafka-based eligibility management:

```
Member Enrollment Event → Kafka Topic → Loyalty-Eligibility Service → Member Database
                                    ↓
                              Real-time Processing
                                    ↓
                         Eligibility Status Update → Kafka Topic → Downstream Services
```

### Implementation Design

#### Kafka Topics
1. **member.enrollment.events**: New member registration events
2. **member.eligibility.updates**: Eligibility status changes
3. **member.family.assignments**: Family member relationship events
4. **eligibility.processing.errors**: Failed eligibility processing events

#### Service Changes

**Loyalty-Eligibility Service Updates**:
- Add Kafka consumer for enrollment events
- Implement real-time eligibility rule engine
- Add spouse auto-assignment logic
- Enhanced dual eligibility conflict resolution

**Loyalty-Member Service Updates**:
- Publish member events to Kafka topics
- Update member status based on eligibility events
- Add family relationship management APIs

#### Database Schema Changes
```sql
-- Add eligibility processing audit table
CREATE TABLE eligibility_processing_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id VARCHAR(36) NOT NULL,
    processing_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    eligibility_rules_applied JSON,
    processing_status VARCHAR(20),
    error_details TEXT,
    INDEX idx_member_timestamp (member_id, processing_timestamp)
);

-- Add spouse assignment tracking
ALTER TABLE loyalty_members 
ADD COLUMN spouse_assignment_status VARCHAR(20) DEFAULT 'PENDING',
ADD COLUMN spouse_assignment_date TIMESTAMP NULL;
```

### Implementation Phases

#### Phase 1: Foundation (Sprint 23)
- Set up Kafka topics and consumer infrastructure
- Implement basic eligibility event processing
- Add comprehensive logging and monitoring
- **Success Criteria**: Process 100% of new enrollments via Kafka

#### Phase 2: Advanced Features (Sprint 24)  
- Implement spouse auto-assignment workflow
- Add dual eligibility conflict resolution
- Performance optimization and load testing
- **Success Criteria**: Reduce spouse assignment failures to <5%

#### Phase 3: Migration Complete (Sprint 25)
- Decommission Top of Funnel script
- Full production cutover to Kafka processing
- Enhanced monitoring and alerting
- **Success Criteria**: Zero dependency on batch processing

### Risk Mitigation

#### Technical Risks
- **Kafka Consumer Lag**: Implement consumer scaling and monitoring
- **Database Performance**: Add appropriate indexes and connection pooling
- **Data Consistency**: Use database transactions and event ordering

#### Operational Risks  
- **Processing Failures**: Implement dead letter queues and retry mechanisms
- **Rollback Strategy**: Keep Top of Funnel script as emergency fallback
- **Monitoring**: Add Splunk dashboards for real-time processing metrics

### Success Metrics
- **Eligibility Processing Time**: < 5 minutes for new enrollments
- **Spouse Assignment Success Rate**: > 95% automatic assignment
- **Dual Eligibility Resolution**: < 2% requiring manual intervention
- **System Uptime**: 99.9% availability for eligibility processing

### Testing Strategy
- Unit tests for all eligibility rule logic
- Integration tests with Kafka test containers
- Performance tests simulating peak enrollment periods
- End-to-end testing in stage environment''',

        'docs/deployment_guide.md': '''# Loyalty Platform Deployment Guide

## Prerequisites
- Access to Optum Kubernetes clusters
- ServiceNow credentials for deployment requests
- VPN connection to on-premises network
- Java 11+ and Maven 3.6+ for local builds

## Environment Overview

### Development Environment
- **Cluster**: k8s-dev-loyalty.optum.com
- **Database**: loyalty-dev-mysql.optum.com:3306
- **Kafka**: kafka-dev-cluster.optum.com:9092
- **Namespace**: loyalty-dev

### Stage Environment  
- **Cluster**: k8s-stage-loyalty.optum.com
- **Database**: loyalty-stage-mysql.optum.com:3306
- **Kafka**: kafka-stage-cluster.optum.com:9092
- **Namespace**: loyalty-stage

### Production Environment
- **Cluster**: k8s-prod-loyalty.optum.com
- **Database**: loyalty-prod-mysql.optum.com:3306
- **Kafka**: kafka-prod-cluster.optum.com:9092
- **Namespace**: loyalty-prod

## Local Development Setup

### Database Connection
```bash
# Connect to development database
mysql -h loyalty-dev-mysql.optum.com -u loyalty_dev_user -p loyalty_dev

# Common development queries
USE loyalty_platform;
SELECT COUNT(*) FROM loyalty_members WHERE status = 'ACTIVE';
SELECT partner, COUNT(*) FROM loyalty_members GROUP BY partner;
```

### Application Configuration
Create `application-local.yml`:
```yaml
spring:
  datasource:
    url: jdbc:mysql://loyalty-dev-mysql.optum.com:3306/loyalty_platform
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  kafka:
    bootstrap-servers: kafka-dev-cluster.optum.com:9092
    consumer:
      group-id: loyalty-member-local
      
logging:
  level:
    com.optum.loyalty: DEBUG
    
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
```

### Running Locally
```bash
# Build the application
mvn clean install

# Set environment variables
export DB_USERNAME=loyalty_dev_user
export DB_PASSWORD=your_dev_password

# Run with local profile
java -jar target/loyalty-member-service-1.0.0.jar --spring.profiles.active=local
```

## Kubernetes Deployment

### Build and Push Docker Image
```bash
# Build Docker image
docker build -t loyalty-member-service:latest .

# Tag for Optum registry
docker tag loyalty-member-service:latest optum-registry.com/loyalty/loyalty-member-service:v1.2.3

# Push to registry
docker push optum-registry.com/loyalty/loyalty-member-service:v1.2.3
```

### Production Deployment Process

### ServiceNow Change Request
1. Create change request in ServiceNow
2. Include deployment artifacts and rollback plan
3. Get approval from Allesha Fogle and Christopher Jimenez
4. Schedule deployment window (typically off-hours)

### Deployment Steps
```bash
# 1. Validate stage environment
curl -f http://loyalty-member-service.loyalty-stage.optum.com/actuator/health

# 2. Deploy to production
kubectl apply -f production-deployment.yaml -n loyalty-prod

# 3. Verify deployment
kubectl rollout status deployment/loyalty-member-service -n loyalty-prod

# 4. Run smoke tests
curl -f http://loyalty-member-service.loyalty-prod.optum.com/actuator/health
curl -f http://loyalty-member-service.loyalty-prod.optum.com/loyalty-member/v1/health
```

### Rollback Procedures
```bash
# Quick rollback to previous version
kubectl rollout undo deployment/loyalty-member-service -n loyalty-prod

# Rollback to specific revision
kubectl rollout undo deployment/loyalty-member-service --to-revision=2 -n loyalty-prod

# Check rollback status
kubectl rollout status deployment/loyalty-member-service -n loyalty-prod
```

## Monitoring and Troubleshooting

### Splunk Queries
```splunk
# Check application logs
index=optum_loyalty source="loyalty-member-service" | head 100

# Monitor error rates  
index=optum_loyalty source="loyalty-member-service" level=ERROR | stats count by message

# Database connection issues
index=optum_loyalty source="loyalty-member-service" "database connection" | head 50
```

### Common Issues
- **Pod Startup Failures**: Check resource limits and database connectivity
- **Database Connection Timeouts**: Verify connection pool configuration
- **Kafka Consumer Lag**: Monitor consumer group status and scaling
- **Memory Issues**: Check heap dump and memory usage patterns''',

        'docs/incident_response.md': '''# Loyalty Platform Incident Response Guide

## Incident Classification

### P1 - Critical
- Production system completely down
- Data corruption affecting member eligibility
- Security breach or data exposure
- **Response Time**: Immediate (within 15 minutes)
- **Escalation**: Automatically page on-call engineer

### P2 - High  
- Partial service degradation
- Dual eligibility processing failures
- Spouse assignment failures affecting >10% of enrollments
- **Response Time**: Within 1 hour
- **Escalation**: Email and Slack notification

### P3 - Medium
- Performance degradation
- Individual member eligibility issues
- Non-critical feature failures
- **Response Time**: Within 4 hours business hours
- **Escalation**: Standard ticket assignment

## Common Incident Scenarios

### Member Eligibility Processing Failures

**Symptoms**:
- New member enrollments not processing
- Members unable to access loyalty platform
- Increased support tickets about eligibility

**Troubleshooting Steps**:
1. Check Kafka consumer lag for eligibility topics
```bash
kubectl exec -it kafka-client -n loyalty-prod -- kafka-consumer-groups.sh \\
  --bootstrap-server kafka-prod-cluster.optum.com:9092 \\
  --describe --group loyalty-eligibility-consumer
```

2. Verify database connectivity
```bash
kubectl exec -it loyalty-member-service-pod -n loyalty-prod -- \\
  mysql -h loyalty-prod-mysql.optum.com -u loyalty_user -p -e "SELECT 1"
```

**Resolution Actions**:
- Restart Kafka consumers if lag is excessive
- Check for database connection pool exhaustion
- Verify Kubernetes pod resource limits
- Review recent deployments for configuration changes

### Dual Eligibility Conflicts

**Symptoms**:
- Members showing multiple active eligibilities
- Point calculation errors
- Support tickets about incorrect reward balances

**Immediate Actions**:
1. Identify affected members
```sql
SELECT member_id, COUNT(*) as eligibility_count 
FROM member_eligibilities 
WHERE status = 'ACTIVE' 
GROUP BY member_id 
HAVING eligibility_count > 1;
```

2. Temporary workaround - disable conflicting eligibility
```sql
UPDATE member_eligibilities 
SET status = 'TEMPORARILY_DISABLED' 
WHERE member_id = 'AFFECTED_MEMBER_ID' 
  AND eligibility_type = 'SECONDARY';
```

3. Engage Taj Mahal team for permanent resolution

### Spouse Assignment Failures

**Symptoms**:
- Family members not linked properly
- New spouses unable to join existing family plans
- Support escalations for family enrollment issues

**Investigation Steps**:
1. Check spouse assignment processing logs
```splunk
index=optum_loyalty source="loyalty-member-service" "spouse assignment" error
```

2. Verify family relationship data
```sql
SELECT family_id, member_id, member_role 
FROM loyalty_members 
WHERE family_id = 'AFFECTED_FAMILY_ID';
```

## Emergency Contacts

### Primary On-Call Rotation
- **Current Week**: Scott Forsmann (612-555-0134)
- **Backup**: Ravali Botta (612-555-0178)
- **Manager Escalation**: Allesha Fogle (612-555-0147)

### Escalation Matrix
1. **Engineering Issues**: On-call engineer → Team Lead → Allesha Fogle
2. **Database Issues**: DBA team (dba-team@optum.com) → Database Manager
3. **Infrastructure**: Platform team → Kubernetes administrators
4. **Security**: security@optum.com → CISO on-call

### Communication Channels
- **Slack**: #loyalty-incidents (immediate response)
- **Email**: loyalty-team@optum.com (status updates)
- **Conference Bridge**: 1-800-555-OPTUM, Code: 123456#

## ServiceNow Integration

### Creating Incident Tickets
1. Log into ServiceNow portal
2. Create new incident with appropriate priority
3. Assign to "Loyalty Platform" assignment group
4. Include affected services and member impact

### Required Information
- **Incident Summary**: Brief description of issue
- **Business Impact**: Number of affected members
- **Steps Taken**: Initial troubleshooting completed
- **Current Status**: Service status and workarounds''',

        'docs/database_setup.md': '''# Loyalty Platform Database Setup Guide

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
```''',

        'docs/LoyaltyMemberService.java': '''package com.optum.loyalty.member.service;

import com.optum.loyalty.member.dto.MemberDTO;
import com.optum.loyalty.member.dto.FamilyMemberDTO;
import com.optum.loyalty.member.entity.LoyaltyMember;
import com.optum.loyalty.member.entity.FamilyMember;
import com.optum.loyalty.member.repository.LoyaltyMemberRepository;
import com.optum.loyalty.member.repository.FamilyMemberRepository;
import com.optum.loyalty.member.kafka.MemberEventProducer;
import com.optum.loyalty.member.exception.MemberNotFoundException;
import com.optum.loyalty.member.exception.DualEligibilityException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Service class for managing loyalty member operations
 * Handles member enrollment, family relationships, and eligibility processing
 * 
 * @author Taj Mahal Team
 * @version 1.2.0
 */
@Service
@Transactional
public class LoyaltyMemberService {
    
    private static final Logger logger = LoggerFactory.getLogger(LoyaltyMemberService.class);
    
    @Autowired
    private LoyaltyMemberRepository memberRepository;
    
    @Autowired
    private FamilyMemberRepository familyMemberRepository;
    
    @Autowired
    private MemberEventProducer memberEventProducer;
    
    /**
     * Retrieves member by UHC member ID
     * @param uhcMemberId UnitedHealthcare member identifier
     * @return MemberDTO containing member details
     * @throws MemberNotFoundException if member not found
     */
    public MemberDTO getMemberByUhcId(String uhcMemberId) {
        logger.info("Retrieving member with UHC ID: {}", uhcMemberId);
        
        Optional<LoyaltyMember> member = memberRepository.findByUhcMemberId(uhcMemberId);
        if (member.isEmpty()) {
            logger.warn("Member not found for UHC ID: {}", uhcMemberId);
            throw new MemberNotFoundException("Member not found with UHC ID: " + uhcMemberId);
        }
        
        return convertToDTO(member.get());
    }
    
    /**
     * Enrolls a new member in the loyalty platform
     * Handles partner/client affiliation and family assignment
     * @param memberDTO Member enrollment details
     * @return Created member DTO
     */
    public MemberDTO enrollMember(MemberDTO memberDTO) {
        logger.info("Enrolling new member: UHC ID {}, Partner: {}, Client: {}", 
                   memberDTO.getUhcMemberId(), memberDTO.getPartner(), memberDTO.getClient());
        
        // Check for existing member
        if (memberRepository.existsByUhcMemberId(memberDTO.getUhcMemberId())) {
            logger.error("Member already exists with UHC ID: {}", memberDTO.getUhcMemberId());
            throw new IllegalArgumentException("Member already enrolled with UHC ID: " + memberDTO.getUhcMemberId());
        }
        
        // Create new member entity
        LoyaltyMember member = new LoyaltyMember();
        member.setMemberId(UUID.randomUUID().toString());
        member.setUhcMemberId(memberDTO.getUhcMemberId());
        member.setPartner(memberDTO.getPartner());
        member.setClient(memberDTO.getClient());
        member.setAffiliation(determineAffiliation(memberDTO));
        member.setEnrollmentDate(LocalDate.now());
        member.setStatus("ACTIVE");
        member.setSpouseAssignmentStatus("PENDING");
        member.setCreatedDate(LocalDateTime.now());
        
        // Handle family assignment
        if (memberDTO.getFamilyId() != null && !memberDTO.getFamilyId().isEmpty()) {
            member.setFamilyId(memberDTO.getFamilyId());
        } else {
            member.setFamilyId(UUID.randomUUID().toString());
        }
        
        // Save member
        LoyaltyMember savedMember = memberRepository.save(member);
        logger.info("Successfully enrolled member: {}", savedMember.getMemberId());
        
        // Publish enrollment event to Kafka
        memberEventProducer.publishMemberEnrollmentEvent(savedMember);
        
        // Process spouse assignment if applicable
        if (memberDTO.getSpouseUhcId() != null) {
            processSpouseAssignment(savedMember, memberDTO.getSpouseUhcId());
        }
        
        return convertToDTO(savedMember);
    }
    
    /**
     * Processes spouse assignment for family enrollment
     * @param primaryMember Primary member in family
     * @param spouseUhcId Spouse's UHC member ID
     */
    private void processSpouseAssignment(LoyaltyMember primaryMember, String spouseUhcId) {
        logger.info("Processing spouse assignment for primary member: {}, spouse UHC ID: {}", 
                   primaryMember.getMemberId(), spouseUhcId);
        
        try {
            // Find spouse by UHC ID
            Optional<LoyaltyMember> spouse = memberRepository.findByUhcMemberId(spouseUhcId);
            
            if (spouse.isPresent()) {
                LoyaltyMember spouseMember = spouse.get();
                
                // Update spouse's family ID
                spouseMember.setFamilyId(primaryMember.getFamilyId());
                spouseMember.setSpouseAssignmentStatus("COMPLETED");
                spouseMember.setSpouseAssignmentDate(LocalDateTime.now());
                memberRepository.save(spouseMember);
                
                // Create family member relationships
                createFamilyMemberRelationship(primaryMember.getFamilyId(), 
                                             primaryMember.getMemberId(), "PRIMARY", true);
                createFamilyMemberRelationship(primaryMember.getFamilyId(), 
                                             spouseMember.getMemberId(), "SPOUSE", false);
                
                // Update primary member status
                primaryMember.setSpouseAssignmentStatus("COMPLETED");
                primaryMember.setSpouseAssignmentDate(LocalDateTime.now());
                memberRepository.save(primaryMember);
                
                // Publish family event
                memberEventProducer.publishFamilyAssignmentEvent(primaryMember.getFamilyId(), 
                                                               primaryMember.getMemberId(), 
                                                               spouseMember.getMemberId());
                
                logger.info("Successfully completed spouse assignment for family: {}", 
                           primaryMember.getFamilyId());
            } else {
                // Spouse not found - mark for retry
                primaryMember.setSpouseAssignmentStatus("SPOUSE_NOT_FOUND");
                memberRepository.save(primaryMember);
                
                logger.warn("Spouse not found for UHC ID: {}, will retry later", spouseUhcId);
            }
            
        } catch (Exception e) {
            // Handle spouse assignment failure
            primaryMember.setSpouseAssignmentStatus("FAILED");
            memberRepository.save(primaryMember);
            
            logger.error("Spouse assignment failed for member: {}, error: {}", 
                        primaryMember.getMemberId(), e.getMessage(), e);
        }
    }
    
    /**
     * Creates family member relationship record
     */
    private void createFamilyMemberRelationship(String familyId, String memberId, 
                                              String relationshipType, boolean isPrimary) {
        FamilyMember familyMember = new FamilyMember();
        familyMember.setFamilyMemberId(UUID.randomUUID().toString());
        familyMember.setFamilyId(familyId);
        familyMember.setMemberId(memberId);
        familyMember.setRelationshipType(relationshipType);
        familyMember.setPrimaryMember(isPrimary);
        familyMember.setCreatedDate(LocalDateTime.now());
        
        familyMemberRepository.save(familyMember);
    }
    
    /**
     * Determines member affiliation based on partner and client
     */
    private String determineAffiliation(MemberDTO memberDTO) {
        String partner = memberDTO.getPartner();
        String client = memberDTO.getClient();
        
        if ("UnitedHealthcare".equals(partner)) {
            if ("INDIVIDUAL".equals(client)) {
                return "UHC_INDIVIDUAL";
            } else if ("FAMILY".equals(client)) {
                return "UHC_FAMILY_PRIMARY";
            }
        } else if ("Optum".equals(partner)) {
            if ("EMPLOYEE".equals(client)) {
                return "OPTUM_EMPLOYEE";
            } else if ("CONTRACTOR".equals(client)) {
                return "OPTUM_CONTRACTOR";
            }
        }
        
        return "UNKNOWN_AFFILIATION";
    }
    
    /**
     * Converts entity to DTO
     */
    private MemberDTO convertToDTO(LoyaltyMember member) {
        MemberDTO dto = new MemberDTO();
        dto.setMemberId(member.getMemberId());
        dto.setUhcMemberId(member.getUhcMemberId());
        dto.setPartner(member.getPartner());
        dto.setClient(member.getClient());
        dto.setAffiliation(member.getAffiliation());
        dto.setEnrollmentDate(member.getEnrollmentDate());
        dto.setStatus(member.getStatus());
        dto.setFamilyId(member.getFamilyId());
        dto.setSpouseAssignmentStatus(member.getSpouseAssignmentStatus());
        return dto;
    }
}'''
    }
    
    # Create each document
    for filepath, content in docs.items():
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"📄 Created {filepath}")

if __name__ == '__main__':
    create_optum_docs()