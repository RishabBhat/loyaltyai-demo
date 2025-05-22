# Optum Loyalty Platform

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
- **Production**: Live member-facing environment