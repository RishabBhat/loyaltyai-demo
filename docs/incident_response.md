# Loyalty Platform Incident Response Guide

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
kubectl exec -it kafka-client -n loyalty-prod -- kafka-consumer-groups.sh \
  --bootstrap-server kafka-prod-cluster.optum.com:9092 \
  --describe --group loyalty-eligibility-consumer
```

2. Verify database connectivity
```bash
kubectl exec -it loyalty-member-service-pod -n loyalty-prod -- \
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
- **Current Status**: Service status and workarounds