# Loyalty-Member Service Documentation

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
