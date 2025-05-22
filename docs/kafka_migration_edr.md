# Engineering Design Record (EDR): Kafka-Based Eligibility Processing

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
- End-to-end testing in stage environment