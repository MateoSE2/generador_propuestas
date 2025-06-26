# Technical Context: SEO Product Description Platform

## Technology Stack

### Backend Stack

```yaml
Core Framework: Django 4.2+ (Python 3.11+)
Database: MySQL 8.0+ with proper indexing and optimization
Cache: Redis 7+ for sessions, job queues, and caching
Message Queue: Celery with Redis broker
Authentication: JWT tokens via microservices integration
ORM: Django ORM with optimized queries and select_related
Migrations: Django migrations system
Testing: pytest-django with factory-boy
API Framework: Django REST Framework
```

### Frontend Stack

```yaml
Framework: React 18+ with TypeScript
State Management: Zustand or Redux Toolkit
UI Components: TailwindCSS + Headless UI or Ant Design
Build Tool: Vite
Testing: Jest + React Testing Library
API Client: TanStack Query (React Query)
```

### Infrastructure Stack

```yaml
Containerization: Docker + Docker Compose (dev), Kubernetes (prod)
Cloud Provider: AWS (primary) or Azure
Database: AWS RDS MySQL or Azure Database for MySQL
Cache/Queue: AWS ElastiCache Redis or Azure Cache for Redis
Storage: AWS S3 or Azure Blob Storage
CDN: CloudFront or Azure CDN
Monitoring: DataDog, New Relic, or Prometheus + Grafana
Microservices: Integration with existing AI assistants platform
User Management: Sync with existing tenant/user management system
```

### Development Tools

```yaml
Code Quality: pre-commit hooks, Black, isort, flake8, mypy
API Documentation: Django REST Framework + drf-spectacular
Version Control: Git with GitFlow branching strategy
CI/CD: GitHub Actions or Azure DevOps
Code Review: Pull Request workflows with required reviews
Plugin Development: WordPress plugin framework (already developed)
```

### WordPress Integration Architecture

```yaml
Integration Type: WordPress Plugin (already developed)
Current State: Unidirectional - fetches product information
Enhancement Needed: Bidirectional sync for generated descriptions
Plugin Location: Separate WordPress plugin codebase
Communication: REST API between WordPress and Django backend
Authentication: API keys or OAuth integration
```

### Microservices Integration

```yaml
Existing Platform: AI assistants app (deployed and operational)
User Management: Centralized user/tenant management service
Authentication: Shared JWT tokens across microservices
Data Sync: Real-time synchronization of user/tenant data
Service Discovery: Kubernetes service mesh or API gateway
Inter-service Communication: REST APIs with circuit breakers
```

## Database Schema Design (MySQL)

### Core Tables

```sql
-- Tenant management (synced with existing system)
CREATE TABLE tenants (
    id CHAR(36) PRIMARY KEY, -- UUID from existing system
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    settings JSON DEFAULT '{}',
    limits JSON DEFAULT '{"monthly_generations": 1000}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_slug (slug),
    INDEX idx_deleted (deleted_at)
);

-- User management (synced with existing system)
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY, -- UUID from existing system
    tenant_id CHAR(36) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    permissions JSON DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    INDEX idx_tenant_email (tenant_id, email),
    INDEX idx_deleted (deleted_at)
);

-- Template management
CREATE TABLE templates (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    prompt TEXT NOT NULL,
    parameters JSON DEFAULT '{}',
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_tenant_default (tenant_id, is_default),
    INDEX idx_deleted (deleted_at)
);

-- Execution tracking
CREATE TABLE executions (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    template_id CHAR(36),
    user_id CHAR(36),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    source_type VARCHAR(50), -- 'excel', 'wordpress'
    source_config JSON,
    total_products INTEGER DEFAULT 0,
    completed_products INTEGER DEFAULT 0,
    failed_products INTEGER DEFAULT 0,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    FOREIGN KEY (template_id) REFERENCES templates(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_tenant_status (tenant_id, status),
    INDEX idx_tenant_created (tenant_id, created_at DESC),
    INDEX idx_status (status)
);

-- Product processing
CREATE TABLE products (
    id CHAR(36) PRIMARY KEY,
    execution_id CHAR(36) NOT NULL,
    external_id VARCHAR(255), -- WordPress product ID, Excel row ID
    original_data JSON NOT NULL,
    generated_content TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    sync_status VARCHAR(50) DEFAULT 'not_synced',
    error_message TEXT,
    llm_usage JSON, -- tokens used, model, cost
    generated_at TIMESTAMP NULL,
    synced_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (execution_id) REFERENCES executions(id),
    INDEX idx_execution_status (execution_id, status),
    INDEX idx_execution_sync (execution_id, sync_status),
    INDEX idx_external_id (external_id),
    FULLTEXT idx_content_search (generated_content)
);

-- Integration management
CREATE TABLE integrations (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'wordpress', 'excel'
    name VARCHAR(255) NOT NULL,
    encrypted_credentials TEXT NOT NULL,
    config JSON DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    INDEX idx_tenant_type (tenant_id, type),
    INDEX idx_deleted (deleted_at)
);

-- Payments tracking (Stripe integration)
CREATE TABLE subscriptions (
    id CHAR(36) PRIMARY KEY,
    tenant_id CHAR(36) NOT NULL,
    stripe_subscription_id VARCHAR(255) UNIQUE NOT NULL,
    stripe_customer_id VARCHAR(255) NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_stripe_subscription (stripe_subscription_id),
    INDEX idx_status (status)
);
```

### Indexes and Performance

```sql
-- Performance indexes
CREATE INDEX idx_tenants_slug ON tenants(slug) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_tenant_email ON users(tenant_id, email) WHERE deleted_at IS NULL;
CREATE INDEX idx_templates_tenant ON templates(tenant_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_executions_tenant_status ON executions(tenant_id, status);
CREATE INDEX idx_executions_tenant_created ON executions(tenant_id, created_at DESC);
CREATE INDEX idx_products_execution_status ON products(execution_id, status);
CREATE INDEX idx_products_execution_sync ON products(execution_id, sync_status);
CREATE INDEX idx_integrations_tenant_type ON integrations(tenant_id, type) WHERE deleted_at IS NULL;

-- Full-text search on generated content
CREATE INDEX idx_products_content_search ON products USING gin(to_tsvector('english', generated_content));
```

## API Architecture

### RESTful API Design

```python
# Base URL structure
/api/v1/tenants/{tenant_id}/...

# Authentication endpoints
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout

# Template management
GET    /api/v1/templates
POST   /api/v1/templates
GET    /api/v1/templates/{template_id}
PUT    /api/v1/templates/{template_id}
DELETE /api/v1/templates/{template_id}

# Execution management
GET    /api/v1/executions
POST   /api/v1/executions
GET    /api/v1/executions/{execution_id}
PUT    /api/v1/executions/{execution_id}
DELETE /api/v1/executions/{execution_id}

# Product operations
GET    /api/v1/executions/{execution_id}/products
POST   /api/v1/executions/{execution_id}/products/{product_id}/regenerate
POST   /api/v1/executions/{execution_id}/products/{product_id}/sync

# Integration management
GET    /api/v1/integrations
POST   /api/v1/integrations
GET    /api/v1/integrations/{integration_id}
PUT    /api/v1/integrations/{integration_id}
DELETE /api/v1/integrations/{integration_id}
POST   /api/v1/integrations/{integration_id}/test
```

### API Response Standards

```python
# Success responses
{
    "success": true,
    "data": {...},
    "meta": {
        "page": 1,
        "per_page": 20,
        "total": 100,
        "total_pages": 5
    }
}

# Error responses
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "field_errors": {
                "email": ["This field is required"]
            }
        }
    }
}
```

## Security Implementation

### Authentication & Authorization

```python
# JWT token structure
{
    "sub": "user_id",
    "tenant_id": "tenant_uuid",
    "role": "admin|user",
    "permissions": ["read", "write", "admin"],
    "exp": 1234567890,
    "iat": 1234567890
}

# Role-based access control
@require_permission("template:write")
async def create_template(current_user: User, template_data: TemplateCreate):
    pass

# Tenant isolation middleware
async def tenant_isolation_middleware(request: Request, call_next):
    tenant_id = extract_tenant_from_token(request)
    request.state.tenant_id = tenant_id
    return await call_next(request)
```

### Data Encryption

```python
# Encryption for sensitive data
class EncryptionService:
    def encrypt_credentials(self, data: dict, tenant_id: str) -> str:
        key = self._get_tenant_key(tenant_id)
        return encrypt_aes_256(json.dumps(data), key)

    def decrypt_credentials(self, encrypted_data: str, tenant_id: str) -> dict:
        key = self._get_tenant_key(tenant_id)
        decrypted = decrypt_aes_256(encrypted_data, key)
        return json.loads(decrypted)
```

## Background Job Processing

### Celery Configuration

```python
# Celery app configuration
from celery import Celery

celery_app = Celery(
    "seo_platform",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.tasks"]
)

# Task configuration
celery_app.conf.update(
    task_serializer="pickle",
    accept_content=["pickle"],
    result_serializer="pickle",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_max_tasks_per_child=1000,
)
```

### Task Definitions

```python
@celery_app.task(bind=True)
def process_generation_job(self, execution_id: str, tenant_id: str):
    """Process a generation job for a specific execution."""
    try:
        execution = get_execution(execution_id, tenant_id)
        products = get_products_for_execution(execution_id)

        for product in products:
            # Update task progress
            self.update_state(
                state="PROGRESS",
                meta={"current": product.index, "total": len(products)}
            )

            # Generate description
            description = generate_description(product, execution.template)

            # Update product with generated content
            update_product_content(product.id, description)

        # Mark execution as completed
        mark_execution_completed(execution_id)

    except Exception as exc:
        # Handle errors and update execution status
        mark_execution_failed(execution_id, str(exc))
        raise self.retry(exc=exc, countdown=60, max_retries=3)
```

## External API Integrations

### WooCommerce API Client

```python
class WooCommerceClient:
    def __init__(self, store_url: str, consumer_key: str, consumer_secret: str):
        self.store_url = store_url.rstrip('/')
        self.auth = HTTPBasicAuth(consumer_key, consumer_secret)
        self.session = httpx.AsyncClient(timeout=30.0)

    async def get_products(
        self,
        page: int = 1,
        per_page: int = 100,
        **filters
    ) -> List[Dict]:
        """Fetch products from WooCommerce."""
        params = {
            "page": page,
            "per_page": per_page,
            **filters
        }

        response = await self.session.get(
            f"{self.store_url}/wp-json/wc/v3/products",
            params=params,
            auth=self.auth
        )
        response.raise_for_status()
        return response.json()

    async def update_product(self, product_id: int, data: Dict) -> Dict:
        """Update a product in WooCommerce."""
        response = await self.session.put(
            f"{self.store_url}/wp-json/wc/v3/products/{product_id}",
            json=data,
            auth=self.auth
        )
        response.raise_for_status()
        return response.json()
```

### LLM Provider Integration

```python
class LLMService:
    def __init__(self, provider: str = "openai"):
        self.provider = self._get_provider(provider)

    async def generate_description(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """Generate product description using LLM."""
        try:
            response = await self.provider.generate(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise

    def _get_provider(self, provider_name: str) -> LLMProvider:
        providers = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "local": LocalLLMProvider()
        }
        return providers.get(provider_name, providers["openai"])
```

## Monitoring and Observability

### Logging Configuration

```python
import structlog

# Structured logging setup
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Usage in application
logger = structlog.get_logger()
logger.info("generation_started",
           tenant_id=tenant_id,
           execution_id=execution_id,
           product_count=len(products))
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint."""
    checks = {
        "database": await check_database_connection(),
        "redis": await check_redis_connection(),
        "external_apis": await check_external_apis()
    }

    status = "healthy" if all(checks.values()) else "unhealthy"

    return {
        "status": status,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Development Workflow

### Local Development Setup

```bash
# Clone repository
git clone <repository-url>
cd seo-platform

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment variables
cp .env.example .env
# Edit .env with local configuration

# Start dependencies
docker-compose up -d postgres redis

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000

# Start Celery worker (separate terminal)
celery -A app.celery_app worker --loglevel=info

# Start frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Testing Strategy

```python
# pytest configuration
# conftest.py
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def test_tenant():
    tenant = await create_test_tenant()
    yield tenant
    await cleanup_test_tenant(tenant.id)

# Example test
async def test_create_template(async_client, test_tenant, auth_headers):
    template_data = {
        "name": "Test Template",
        "prompt": "Generate description for {{product_name}}"
    }

    response = await async_client.post(
        f"/api/v1/templates",
        json=template_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    assert response.json()["data"]["name"] == "Test Template"
```

This technical context provides the foundation for implementing a robust, scalable, and maintainable SaaS platform.
