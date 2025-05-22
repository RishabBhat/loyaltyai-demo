# Loyalty Platform Deployment Guide

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
- **Memory Issues**: Check heap dump and memory usage patterns