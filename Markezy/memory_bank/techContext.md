# Tech Context - Markezy

## Team Skill Set

### Development Team Capabilities

- **Python Expertise**: Strong Django framework experience
- **Frontend Development**: React with JavaScript/TypeScript proficiency
- **Database Management**: MySQL administration and optimization
- **Containerization**: Docker and Docker Compose experience
- **API Integration**: REST API development and third-party integration experience

### DevOps and Infrastructure

- **Linux Server Management**: VPS administration and maintenance
- **Git Workflows**: Version control and CI/CD pipeline management
- **Container Orchestration**: Docker Swarm deployment patterns
- **Monitoring**: Basic application and infrastructure monitoring
- **Security**: HTTPS, JWT authentication, and basic security practices

### AI and Integration Skills

- **OpenAI API**: Prompt engineering and API integration
- **Vector Databases**: Qdrant setup and query optimization
- **CRM Integration**: Clientify API and webhook management
- **Background Processing**: Celery and Redis queue management

## Deployment Constraints

### Infrastructure Limitations

- **Single VPS**: IONOS dedicated Linux server for both staging and production
- **Resource Constraints**: Shared resources between staging and production environments
- **Network Configuration**: Standard VPS networking without advanced load balancing
- **Storage**: Local disk storage with regular backup requirements

### Deployment Requirements

- **Zero-Downtime Deployments**: Git-based deployment with minimal service interruption
- **Environment Separation**: Clear isolation between staging and production
- **Rollback Capability**: Quick rollback to previous version if issues arise
- **Security Updates**: Regular OS and dependency updates without breaking changes

### Performance Constraints

- **Concurrent Users**: Must support 5+ concurrent conversations minimum
- **Response Times**: P95 response time under 2 seconds
- **Storage Growth**: Plan for lead data and document storage growth
- **Bandwidth**: Efficient data transfer for PDF downloads and API calls

## Technology Stack (Fixed Requirements)

### Backend Infrastructure

- **Runtime**: Python 3.12 in Docker containers
- **Web Framework**: Django with Django REST Framework
- **Task Queue**: Celery with Redis broker
- **Database**: MySQL for primary data storage
- **Caching**: Redis for session management and caching

### Frontend Technology

- **Framework**: React with modern JavaScript/TypeScript
- **Build Tools**: Standard React build pipeline
- **State Management**: Context API or Redux for complex state
- **UI Components**: Component library for consistent design
- **Mobile Responsive**: Progressive Web App capabilities

### AI and Data Processing

- **Language Model**: OpenAI API for strategy generation
- **Vector Store**: Qdrant for semantic search and content retrieval
- **Document Generation**: PDF creation libraries for strategy documents
- **Natural Language**: Spanish language processing and optimization

### Infrastructure and Deployment

- **Containerization**: Docker Compose for local development
- **Container Orchestration**: Docker Swarm for production deployment
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Monitoring**: Container health checks and basic metrics collection

## Integration Architecture

### Required External Integrations

- **Clientify CRM**: Real-time lead data synchronization
- **OpenAI API**: Strategy generation and conversational AI
- **Email Service**: SMTP or service like SendGrid for notifications
- **File Storage**: Local storage with backup strategy

### Optional Future Integrations

- **byNeural**: Historic lead import (one-time migration)
- **Stripe**: Payment processing for agency subscriptions
- **Google Analytics**: User behavior tracking and conversion metrics
- **WordPress**: Embeddable widget for agency websites

### API Design Principles

- **RESTful Endpoints**: Standard HTTP methods and status codes
- **JSON Communication**: Consistent JSON request/response format
- **Authentication**: JWT-based API authentication
- **Rate Limiting**: Protection against API abuse
- **Versioning**: API version management for backward compatibility

## Security and Compliance

### Data Protection Requirements

- **RGPD Compliance**: Full compliance with EU data protection regulations
- **Data Encryption**: Encryption at rest and in transit
- **Access Controls**: Role-based access with audit trails
- **Consent Management**: Explicit consent tracking with timestamps
- **Data Retention**: Configurable data retention policies

### Security Implementation

- **HTTPS Enforcement**: SSL/TLS certificates for all communications
- **JWT Security**: Secure token generation and validation
- **Input Validation**: Protection against injection attacks
- **CORS Configuration**: Proper cross-origin resource sharing setup
- **Security Headers**: Implementation of security-focused HTTP headers

### Backup and Recovery

- **Database Backups**: Regular automated database backups
- **File Backups**: PDF documents and uploaded files backup
- **Recovery Testing**: Regular restore testing of backup systems
- **Disaster Recovery**: Plan for server failure and data recovery

## Development and Testing

### Development Environment

- **Local Setup**: Docker Compose for complete local development
- **Environment Variables**: Configuration management for different environments
- **Database Seeding**: Sample data for development and testing
- **Hot Reloading**: Fast development iteration with live reloading

### Testing Strategy

- **Unit Tests**: Python unittest and Django testing framework
- **Integration Tests**: API endpoint testing with real database
- **Frontend Testing**: React component testing with Jest
- **End-to-End Testing**: User journey testing for critical paths

### Quality Assurance

- **Code Review**: Pull request review process
- **Linting**: Python (flake8, black) and JavaScript (ESLint, Prettier)
- **Type Checking**: TypeScript for frontend type safety
- **Security Scanning**: Automated dependency vulnerability scanning

## Monitoring and Analytics

### Application Monitoring

- **Health Endpoints**: Service health check endpoints
- **Error Tracking**: Centralized error logging and alerting
- **Performance Metrics**: Response time and throughput monitoring
- **Resource Usage**: CPU, memory, and disk usage tracking

### Business Analytics

- **User Activity**: Track feature usage and user engagement
- **Conversion Metrics**: Lead qualification and conversion rates
- **Performance KPIs**: Strategy quality and client satisfaction metrics
- **Revenue Attribution**: Track leads to actual business outcomes

### Operational Metrics

- **System Uptime**: Service availability tracking
- **API Performance**: External integration health and performance
- **Database Performance**: Query performance and connection health
- **Storage Metrics**: Disk usage and backup success tracking
