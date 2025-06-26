# System Patterns: SEO Product Description Platform

## Architectural Patterns

### Multi-Tenant SaaS Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                API Gateway                              │
│             (Tenant Routing)                            │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│              Application Layer                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │   Web UI    │ │   API       │ │   Workers   │      │
│  │   (React)   │ │  (FastAPI)  │ │  (Celery)   │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                Data Layer                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │ PostgreSQL  │ │    Redis    │ │   S3/Blob   │      │
│  │ (App Data)  │ │   (Cache)   │ │  (Files)    │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### Tenant Isolation Strategy

- **Shared Database, Tenant-Scoped Queries**: Cost-effective, secure row-level isolation
- **Tenant Context Injection**: Middleware ensures all queries include tenant_id
- **Resource Limits**: Per-tenant quotas for API calls, storage, and processing

### Microservices Architecture (Integrated with Existing Platform)

```
┌─────────────────────────────────────────────────────────┐
│                 Existing AI Assistants Platform        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │    User     │ │   Tenant    │ │    Auth     │      │
│  │ Management  │ │ Management  │ │  Service    │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
└─────────────────┬───────────────────────────────────────┘
                  │ (JWT Tokens & User/Tenant Sync)
┌─────────────────▼───────────────────────────────────────┐
│              SEO Description Platform                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │   Web App   │ │  Django     │ │   Celery    │      │
│  │  (React)    │ │   API       │ │  Workers    │      │
│  └─────────────┘ └─────────────┘ └─────────────┘      │
└─────────────────┬───────────────────────────────────────┘
                  │
      ┌───────────┼───────────────┐
      │           │               │
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ WordPress   │ │    Excel    │ │   Stripe    │
│   Plugin    │ │  Processing │ │  Payments   │
│ (Enhanced)  │ │   Service   │ │  Service    │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Design Patterns

### Repository Pattern

```python
# Abstract Repository
class BaseRepository:
    def get_by_tenant(self, tenant_id: str, entity_id: str)
    def create(self, tenant_id: str, entity: BaseEntity)
    def update(self, tenant_id: str, entity: BaseEntity)
    def delete(self, tenant_id: str, entity_id: str)

# Concrete Implementation
class ExecutionRepository(BaseRepository):
    def get_active_jobs(self, tenant_id: str) -> List[Execution]
    def get_by_status(self, tenant_id: str, status: str) -> List[Execution]
```

### Factory Pattern for LLM Providers

```python
class LLMProviderFactory:
    @staticmethod
    def create_provider(provider_type: str, config: dict) -> LLMProvider:
        if provider_type == "openai":
            return OpenAIProvider(config)
        elif provider_type == "anthropic":
            return AnthropicProvider(config)
        # ...
```

### Observer Pattern for Job Status Updates

```python
class JobStatusObserver:
    def on_job_started(self, job: Execution)
    def on_job_completed(self, job: Execution)
    def on_job_failed(self, job: Execution)

# Real-time UI updates, email notifications, webhooks
```

### Strategy Pattern for Sync Operations

```python
class SyncStrategy:
    def sync_to_store(self, products: List[Product], credentials: StoreCredentials)

class WooCommerceSyncStrategy(SyncStrategy):
    def sync_to_store(self, products: List[Product], credentials: WooCommerceCredentials)
```

## Data Management Patterns

### Entity-Relationship Design

```sql
-- Core Entities
tenants (id, name, settings, created_at)
users (id, tenant_id, email, role, permissions)
templates (id, tenant_id, name, prompt, parameters)
executions (id, tenant_id, template_id, status, created_at)
products (id, execution_id, original_data, generated_content, sync_status)
integrations (id, tenant_id, type, credentials, config)

-- Relationships
users.tenant_id → tenants.id
templates.tenant_id → tenants.id
executions.tenant_id → tenants.id
executions.template_id → templates.id
products.execution_id → executions.id
integrations.tenant_id → tenants.id
```

### Audit Trail Pattern

```sql
-- Every operation tracked
audit_logs (
    id, tenant_id, user_id, entity_type, entity_id,
    action, old_values, new_values, timestamp
)
```

### Soft Delete Pattern

```sql
-- All entities support soft deletion
deleted_at TIMESTAMP NULL
-- Queries automatically filter WHERE deleted_at IS NULL
```

## Security Patterns

### Multi-Tenant Security

- **Row-Level Security (RLS)**: Database-enforced tenant isolation
- **JWT Token Scoping**: Tokens include tenant_id claim
- **API Middleware**: Automatic tenant context injection
- **Resource Ownership**: All resources explicitly owned by tenant

### Credential Management

```python
# Encrypted credential storage
class EncryptedCredentials:
    def encrypt(self, credentials: dict, tenant_id: str) -> str
    def decrypt(self, encrypted_data: str, tenant_id: str) -> dict

# Per-tenant encryption keys
tenant_encryption_keys (tenant_id, key_hash, created_at)
```

### Rate Limiting Pattern

```python
# Per-tenant rate limiting
@rate_limit(key="tenant:{tenant_id}", rate="100/hour")
async def generate_descriptions(tenant_id: str, products: List[Product])
```

## Integration Patterns

### WooCommerce API Client

```python
class WooCommerceClient:
    def __init__(self, store_url: str, api_key: str, api_secret: str)

    async def get_products(self, **filters) -> List[WooProduct]
    async def update_product(self, product_id: int, data: dict) -> WooProduct
    async def batch_update(self, updates: List[dict]) -> BatchResult

    # Retry logic, rate limiting, error handling built-in
```

### Internet Search Integration

```python
class ContextEnrichmentService:
    async def enrich_product(self, product: Product) -> EnrichedProduct:
        search_results = await self._search_internet(product.name)
        filtered_results = self._filter_trusted_sources(search_results)
        return self._merge_context(product, filtered_results)
```

## Scalability Patterns

### Horizontal Scaling

- **Stateless Services**: All services can scale horizontally
- **Load Balancing**: Distribute requests across instances
- **Database Sharding**: Future-ready for tenant-based sharding

### Caching Strategy

```python
# Multi-level caching
L1: In-memory (per-process)
L2: Redis (shared)
L3: Database query cache

# Cache invalidation patterns
@cache_invalidate(keys=["tenant:{tenant_id}:templates"])
async def update_template(tenant_id: str, template: Template)
```

### Queue Management

```python
# Priority-based job queues
high_priority_queue: Premium tenant jobs
normal_queue: Standard tenant jobs
low_priority_queue: Batch/background jobs

# Auto-scaling based on queue depth
```

## Error Handling Patterns

### Resilience Patterns

```python
# Circuit Breaker for external APIs
@circuit_breaker(failure_threshold=5, recovery_timeout=60)
async def call_llm_api(prompt: str) -> str

# Retry with exponential backoff
@retry(max_attempts=3, backoff=exponential_backoff)
async def sync_to_woocommerce(product: Product)

# Graceful degradation
async def generate_description_with_fallback(product: Product) -> str:
    try:
        return await premium_llm_generate(product)
    except Exception:
        return await basic_template_generate(product)
```

### Monitoring and Observability

```python
# Structured logging
logger.info("job_started", extra={
    "tenant_id": tenant_id,
    "job_id": job_id,
    "product_count": len(products)
})

# Metrics collection
metrics.counter("llm_api_calls").increment()
metrics.histogram("job_duration_seconds").observe(duration)

# Distributed tracing
@trace("generate_descriptions")
async def generate_descriptions(products: List[Product])
```

## Performance Patterns

### Database Query Optimization

```sql
-- Tenant-aware indexes
CREATE INDEX idx_executions_tenant_status ON executions(tenant_id, status);
CREATE INDEX idx_products_execution_sync ON products(execution_id, sync_status);

-- Pagination patterns
SELECT * FROM executions
WHERE tenant_id = ? AND created_at < ?
ORDER BY created_at DESC
LIMIT 20;
```

### Batch Processing Optimization

```python
# Batch operations to reduce API calls
async def batch_generate(products: List[Product], batch_size: int = 10):
    for batch in chunks(products, batch_size):
        await asyncio.gather(*[generate_single(p) for p in batch])
```

## Microservices Integration Patterns

### User/Tenant Synchronization Pattern

```python
# User sync service pattern
class UserSyncService:
    def __init__(self, ai_assistants_api_client):
        self.ai_assistants_client = ai_assistants_api_client

    async def sync_user_data(self, user_uuid: str):
        """Sync user data from AI assistants platform"""
        user_data = await self.ai_assistants_client.get_user(user_uuid)
        local_user = await self.create_or_update_local_user(user_data)
        return local_user

    async def sync_tenant_data(self, tenant_uuid: str):
        """Sync tenant data from AI assistants platform"""
        tenant_data = await self.ai_assistants_client.get_tenant(tenant_uuid)
        local_tenant = await self.create_or_update_local_tenant(tenant_data)
        return local_tenant
```

### JWT Integration Pattern

```python
# JWT middleware for microservices
class MicroservicesAuthMiddleware:
    def __init__(self, ai_assistants_jwt_validator):
        self.jwt_validator = ai_assistants_jwt_validator

    async def __call__(self, request, call_next):
        # Extract JWT from existing AI assistants platform
        token = self.extract_jwt_token(request)

        # Validate with shared secret/public key
        payload = await self.jwt_validator.validate(token)

        # Extract tenant and user info
        request.state.user_id = payload.get('sub')
        request.state.tenant_id = payload.get('tenant_id')
        request.state.permissions = payload.get('permissions', [])

        return await call_next(request)
```

### Service Communication Pattern

```python
# Inter-service communication with circuit breaker
class AIAssistantsApiClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=timeout)

    @circuit_breaker(failure_threshold=5, recovery_timeout=60)
    async def get_user(self, user_uuid: str) -> Dict:
        """Get user data from AI assistants platform"""
        response = await self.client.get(
            f"{self.base_url}/api/users/{user_uuid}",
            headers=self.get_service_auth_headers()
        )
        response.raise_for_status()
        return response.json()

    @circuit_breaker(failure_threshold=5, recovery_timeout=60)
    async def get_tenant(self, tenant_uuid: str) -> Dict:
        """Get tenant data from AI assistants platform"""
        response = await self.client.get(
            f"{self.base_url}/api/tenants/{tenant_uuid}",
            headers=self.get_service_auth_headers()
        )
        response.raise_for_status()
        return response.json()
```

### WordPress Plugin Integration Pattern

```php
// WordPress plugin enhancement pattern
class SEODescriptionPlugin {
    private $django_api_base_url;
    private $api_credentials;

    public function __construct() {
        // Existing plugin functionality
        $this->django_api_base_url = get_option('seo_description_api_url');
        $this->api_credentials = get_option('seo_description_api_credentials');

        // Add new bidirectional sync hooks
        add_action('rest_api_init', array($this, 'register_api_endpoints'));
        add_action('wp_ajax_sync_descriptions', array($this, 'handle_sync_request'));
    }

    // Existing unidirectional functionality (fetch products)
    public function fetch_products_for_sync() {
        // Already implemented - fetches product data
        return $this->get_woocommerce_products();
    }

    // NEW: Bidirectional sync functionality
    public function register_api_endpoints() {
        register_rest_route('seo-description/v1', '/receive-descriptions', array(
            'methods' => 'POST',
            'callback' => array($this, 'receive_generated_descriptions'),
            'permission_callback' => array($this, 'verify_django_api_request'),
        ));
    }

    public function receive_generated_descriptions($request) {
        $descriptions = $request->get_json_params();

        foreach ($descriptions as $product_data) {
            $this->update_product_description(
                $product_data['product_id'],
                $product_data['generated_description']
            );
        }

        return new WP_REST_Response(array(
            'success' => true,
            'updated_count' => count($descriptions)
        ), 200);
    }
}
```

### Feature-Based Database Pattern

```python
# Feature-based database organization
class FeatureBasedModels:
    """Organize models by feature for better cost tracking"""

    # Foundation Feature Models
    class UserSync(models.Model):
        external_user_id = models.CharField(max_length=36)  # From AI assistants
        tenant_id = models.CharField(max_length=36)
        synced_at = models.DateTimeField(auto_now=True)

    # Simple Dashboard Feature Models
    class DashboardMetric(models.Model):
        tenant_id = models.CharField(max_length=36)
        metric_type = models.CharField(max_length=50)
        value = models.JSONField()
        calculated_at = models.DateTimeField(auto_now=True)

    # Parametrization Feature Models
    class Template(models.Model):
        tenant_id = models.CharField(max_length=36)
        name = models.CharField(max_length=255)
        prompt = models.TextField()
        parameters = models.JSONField(default=dict)
        feature_version = models.CharField(max_length=20)  # Track feature complexity

    # WordPress Integration Feature Models
    class WordPressIntegration(models.Model):
        tenant_id = models.CharField(max_length=36)
        site_url = models.URLField()
        plugin_version = models.CharField(max_length=20)
        sync_status = models.CharField(max_length=50)
        last_bidirectional_sync = models.DateTimeField(null=True)
```

### Cost Tracking Pattern

```python
# Feature-based cost tracking
class FeatureCostTracker:
    def __init__(self):
        self.feature_costs = {
            'user_management': {'budget': 3000, 'spent': 0},
            'simple_dashboard': {'budget': 2000, 'spent': 0},
            'simple_parametrization': {'budget': 2500, 'spent': 0},
            'wordpress_integration': {'budget': 3750, 'spent': 750},  # 20% done
            'excel_integration': {'budget': 3000, 'spent': 0},
            'complex_dashboard': {'budget': 5000, 'spent': 0},
            'complex_parametrization': {'budget': 4250, 'spent': 0},
            'stripe_payments': {'budget': 2500, 'spent': 0},
        }

    def track_feature_progress(self, feature_name: str, hours_spent: float, hourly_rate: float = 75):
        cost = hours_spent * hourly_rate
        self.feature_costs[feature_name]['spent'] += cost
        return {
            'feature': feature_name,
            'budget': self.feature_costs[feature_name]['budget'],
            'spent': self.feature_costs[feature_name]['spent'],
            'remaining': self.feature_costs[feature_name]['budget'] - self.feature_costs[feature_name]['spent'],
            'percentage_complete': (self.feature_costs[feature_name]['spent'] / self.feature_costs[feature_name]['budget']) * 100
        }
```

These patterns ensure the system integrates seamlessly with the existing AI assistants platform while maintaining feature-based development and cost tracking capabilities.
