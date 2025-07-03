# Tech Context - AISearch_WorldShishas

## Technology Stack

### Backend

- **Framework**: Django 3.2 (byNeural existing infrastructure)
- **Task Queue**: Celery for asynchronous processing
- **Message Broker**: Redis for Celery and caching
- **Database**: MySQL (existing byNeural setup)
- **Containerization**: Docker containers for all services

### Frontend

- **Framework**: React/TypeScript embedded as WordPress plugin
- **Build System**: Webpack for bundling and optimization
- **Styling**: CSS Modules or Styled Components (encapsulated)
- **Package Management**: npm/yarn for dependency management

### AI & Search

- **Language Model**: OpenAI API for semantic understanding
- **Vector Store**: Qdrant for similarity search
- **Search Strategy**: Hybrid (exact keyword + semantic vector search)
- **Embeddings**: OpenAI text-embedding-ada-002

### Infrastructure

- **Containerization**: Docker Compose for development and deployment
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Environment Management**: Docker environments (dev, staging, prod)
- **Monitoring**: Basic logging and error tracking

## Technical Requirements

### WordPress Integration

- **Minimum Version**: WordPress 6.0+
- **PHP Version**: PHP 8.0+
- **Plugin Format**: Installable ZIP package
- **Distribution**: Self-contained with all dependencies
- **Compatibility**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)

### API Integration

- **Protocol**: REST API with JSON payloads
- **Authentication**: API key-based authentication
- **Endpoint**: `/api/v1/hybrid-search/` on byNeural infrastructure
- **Response Format**: Standardized JSON with product data
- **Error Handling**: HTTP status codes with descriptive messages

### Performance Requirements

- **Response Time**: ≤ 2 seconds for 5 search results
- **Availability**: 99% monthly uptime (inherited from byNeural SLA)
- **Concurrency**: Support multiple simultaneous search requests
- **Caching**: WordPress transients for frequent queries

### Security Requirements

- **Transport Security**: HTTPS enforced for all API communications
- **Input Validation**: Sanitization of all search queries
- **Rate Limiting**: Protection against abuse and excessive requests
- **Data Privacy**: No storage of personal search data in MVP

## Development Environment

### Local Setup

- **Container Stack**: Docker Compose with services:
  - Django application server
  - MySQL database
  - Redis message broker
  - Qdrant vector database
- **WordPress**: Local WordPress installation for plugin testing
- **Tools**: Docker, npm/yarn, git

### Development Workflow

- **Version Control**: Git with feature branch workflow
- **Testing**: Unit tests for API endpoints, integration tests for search functionality
- **Code Quality**: ESLint for TypeScript, Black for Python
- **Documentation**: Inline code documentation and API specification

## Deployment Architecture

### Production Setup

- **Container Orchestration**: Docker Compose on dedicated server
- **Load Balancing**: Nginx reverse proxy (if needed)
- **Database**: MySQL container with persistent volumes
- **Redis**: Redis container for caching and task queue
- **Monitoring**: Basic container health checks

### CI/CD Pipeline

- **Trigger**: Git push to main branch
- **Steps**:
  1. Run automated tests
  2. Build Docker images
  3. Deploy to staging environment
  4. Run integration tests
  5. Deploy to production (manual approval)
- **Rollback**: Previous Docker image deployment capability

## Integration Points

### byNeural API Integration

- **Existing Services**: Leverage current RAG infrastructure
- **New Endpoints**: Extend API with hybrid search capability
- **Data Sync**: Use existing product database
- **Authentication**: Extend current API authentication system

### WordPress Integration

- **Plugin Installation**: Standard WordPress plugin installation process
- **Configuration**: Admin panel for basic settings (API endpoint, credentials)
- **Shortcode Support**: Optional shortcode for custom placements
- **Theme Compatibility**: CSS isolation to prevent conflicts

### External Dependencies

- **OpenAI API**: For text embeddings and semantic processing
- **Qdrant**: Vector database for similarity search
- **WordPress APIs**: For plugin functionality and data access
- **Browser APIs**: For modern JavaScript functionality

## Constraints and Considerations

### Technical Constraints

- **WordPress Compatibility**: Must work with existing WordPress themes
- **Plugin Size**: Reasonable bundle size for web distribution
- **Browser Support**: Modern browsers only (no IE11 support)
- **Mobile Responsive**: Must work on mobile devices

### Operational Constraints

- **No Breaking Changes**: Cannot modify existing byNeural functionality
- **Minimal WordPress Changes**: Plugin should be self-contained
- **Resource Usage**: Reasonable server resource consumption
- **Backup Strategy**: Standard Docker volume backup procedures

### Language and Localization

- **Primary Language**: Spanish (Spain)
- **Character Encoding**: UTF-8 throughout the system
- **Future i18n**: Code prepared for internationalization
- **Text Content**: All user-facing text in Spanish
