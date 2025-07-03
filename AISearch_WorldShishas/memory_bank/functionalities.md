# Functionalities - AISearch_WorldShishas

**Last Updated**: 2025-06-30  
**Status**: Complete Functional Specification

## 1. Hybrid Search API Endpoint

### Title

**Intelligent Hybrid Search Service**

### Detailed Description

**Purpose**: Provide a unified search endpoint that combines exact keyword matching with AI-powered semantic search to deliver more relevant and comprehensive product discovery results.

**User Stories**:

- As a WordPress site visitor, I want to search using natural language so that I can find products even when I don't know exact product names
- As a site visitor, I want to find products by describing characteristics (e.g., "sabor fuerte", "cachimba pequeña") so that discovery is intuitive
- As a developer, I want a reliable API endpoint that consistently delivers search results in under 2 seconds

**Acceptance Criteria**:

- Endpoint `/api/v1/hybrid-search/` accepts POST requests with JSON payload
- Request format: `{"query": "string", "limit": integer, "offset": integer}`
- Response includes weighted combination of exact matches + semantic similarities
- Response format: `{"results": [...], "total": int, "has_more": bool, "query_time": float}`
- Each result includes: `id, nombre, precio, imagen_url, product_url, relevance_score`
- API response time ≤ 2 seconds for 5-10 results
- Fallback to exact search if vector search fails
- Input validation and sanitization for all queries
- Rate limiting: 100 requests per minute per IP

**Data Notes**:

- Product data sourced from existing MySQL WordPress database
- Vector embeddings generated using OpenAI text-embedding-ada-002
- Weighted scoring: 60% exact match + 40% semantic similarity (configurable)
- Minimum query length: 2 characters, maximum: 200 characters

**Edge Cases**:

- Empty query returns error message
- No results found returns empty array with appropriate message
- Special characters and emojis are properly handled
- Timeout scenarios trigger fallback mechanism

### Status Flag

`CORE`

### Dependencies & Integrations

- **Internal**: byNeural Django infrastructure, MySQL product database
- **External**: OpenAI API for embeddings, Qdrant vector database
- **Services**: Redis for caching frequent queries
- **Infrastructure**: Docker containers for Qdrant deployment

### Non-functional Requirements

- **Performance**: Sub-2-second response time, support 50 concurrent requests
- **Reliability**: 99% uptime, graceful degradation if vector search unavailable
- **Security**: API key authentication, request rate limiting, input sanitization
- **Scalability**: Horizontal scaling ready with container orchestration

---

## 2. WordPress Search Plugin

### Title

**Intelligent Search WordPress Plugin**

### Detailed Description

**Purpose**: Provide a modern, user-friendly search interface that integrates seamlessly with existing WordPress themes while delivering enhanced search capabilities through the hybrid API.

**User Stories**:

- As a WordPress site visitor, I want a prominent search bar that's easy to find and use
- As a visitor, I want search results displayed in an attractive modal without leaving the current page
- As a visitor, I want to see loading indicators when search is in progress
- As a site administrator, I want to install the plugin easily without breaking my existing theme

**Acceptance Criteria**:

- **Search Bar Component**:

  - Responsive design that adapts to different screen sizes
  - Placeholder text "Buscar productos..." with search icon
  - Minimum 3-character trigger for search execution
  - Debounced input (300ms delay) to prevent excessive API calls
  - Enter key and search icon both trigger search

- **Modal Interface**:

  - Dark backdrop overlay with smooth fade-in animation
  - Centered modal with modern card-style design
  - Search input field maintains focus when modal opens
  - Close options: ESC key, backdrop click, X button
  - Responsive design for mobile and desktop

- **Results Display**:

  - Initial display shows 5 search results
  - Each result shows: product image, name, price, direct link
  - "Sin resultados" message for empty result sets
  - "Error de conexión" message for API failures
  - "Cargar más" button for pagination (loads additional 5 results)
  - Loading spinner with "Buscando..." text during API calls

- **Plugin Installation**:
  - Distributed as installable ZIP file
  - Self-contained with all dependencies bundled
  - Automatic activation of search functionality
  - Optional shortcode `[ai_search_bar]` for custom placement
  - Admin settings page for API configuration

**Technical Implementation**:

- React/TypeScript components with modern hooks
- CSS-in-JS or CSS Modules for style encapsulation
- Webpack bundling for production optimization
- WordPress REST API integration
- Progressive enhancement (works without JavaScript)

**Design Requirements**:

- Consistent with modern WordPress admin aesthetics
- Spanish language interface
- Accessible color contrast ratios
- Mobile-first responsive design
- Loading states and micro-interactions

### Status Flag

`CORE`

### Dependencies & Integrations

- **Internal**: Hybrid Search API endpoint
- **WordPress**: WordPress 6.0+, PHP 8.0+
- **Build Tools**: Node.js, Webpack, TypeScript compiler
- **External**: Modern browser capabilities (ES6+, Fetch API)

### Non-functional Requirements

- **Performance**: Modal opens in <200ms, search results render in <100ms after API response
- **Compatibility**: Works with popular WordPress themes without conflicts
- **Accessibility**: Keyboard navigation, screen reader compatible (basic level)
- **Browser Support**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

---

## 3. Search Result Optimization

### Title

**Weighted Result Scoring & Ranking**

### Detailed Description

**Purpose**: Deliver the most relevant search results by intelligently combining exact keyword matches with semantic similarity scores, ensuring users find what they're looking for quickly.

**User Stories**:

- As a user searching for "cachimba azul", I want to see exact color matches first, then semantically similar products
- As a user searching for "regalo principiante", I want products suitable for beginners even if they don't contain those exact words
- As a user, I want consistent result quality regardless of how I phrase my search query

**Acceptance Criteria**:

- **Scoring Algorithm**:

  - Exact match scoring based on: product name (weight: 1.0), category (weight: 0.8), tags (weight: 0.6)
  - Semantic similarity using vector cosine similarity
  - Combined score: (exact*score * 0.6) + (semantic*score * 0.4)
  - Results sorted by combined relevance score (descending)
  - Minimum relevance threshold: 0.3 (configurable)

- **Result Deduplication**:

  - Remove duplicate products from combined results
  - Preserve highest-scoring instance of duplicates
  - Maintain result ordering based on final scores

- **Quality Assurance**:
  - A/B testing capability for different weight configurations
  - Relevance scoring feedback mechanism (future enhancement)
  - Query performance logging for optimization

**Configuration Options**:

- Adjustable weight parameters via environment variables
- Configurable result limits and pagination sizes
- Minimum query length and maximum query constraints

### Status Flag

`CORE`

### Dependencies & Integrations

- **Internal**: Product database schema, search API endpoint
- **External**: Vector similarity computation algorithms
- **Infrastructure**: Redis caching for performance optimization

### Non-functional Requirements

- **Performance**: Scoring computation adds <100ms to overall response time
- **Consistency**: Identical queries return identical result ordering
- **Configurability**: Weight adjustments without code deployment

---

## 4. Error Handling & User Feedback

### Title

**Comprehensive Error Management System**

### Detailed Description

**Purpose**: Provide clear, actionable feedback to users when searches fail, APIs are unavailable, or unexpected errors occur, maintaining a positive user experience even during system issues.

**User Stories**:

- As a user, I want clear messages when my search doesn't return results so I know what to try next
- As a user, I want to know when there's a technical problem so I don't think the search is broken
- As a user, I want the system to retry automatically when appropriate

**Acceptance Criteria**:

- **Error Categories & Messages**:

  - No Results: "No se encontraron productos para tu búsqueda. Intenta con otros términos."
  - API Timeout: "La búsqueda está tardando más de lo esperado. Por favor, inténtalo de nuevo."
  - Connection Error: "Error de conexión. Verifica tu conexión a internet e inténtalo de nuevo."
  - Server Error: "Problema temporal del servidor. Inténtalo de nuevo en unos momentos."
  - Invalid Query: "Por favor, introduce al menos 2 caracteres para buscar."

- **Error Recovery**:

  - Automatic retry for timeout errors (max 2 attempts)
  - Fallback to cached results when available
  - Clear error state when new search is initiated
  - Graceful degradation to basic WordPress search if API completely unavailable

- **User Experience**:
  - Error messages displayed in search modal
  - Non-intrusive error styling (not aggressive red alerts)
  - Suggested actions provided where appropriate
  - Loading states properly cleared on error conditions

### Status Flag

`CORE`

### Dependencies & Integrations

- **Internal**: API monitoring and health checks
- **Infrastructure**: Logging system for error tracking
- **UX**: Consistent with overall plugin design system

### Non-functional Requirements

- **Reliability**: Error handling doesn't cause crashes or infinite loops
- **Observability**: All errors logged with appropriate context for debugging
- **Recovery**: System automatically returns to normal operation when conditions improve

---

## 5. Performance Optimization

### Title

**Search Performance & Caching System**

### Detailed Description

**Purpose**: Ensure consistent sub-2-second search performance through intelligent caching, query optimization, and resource management strategies.

**User Stories**:

- As a user, I want search results to appear quickly so I don't lose interest
- As a frequent user, I want repeated searches to be even faster
- As a site owner, I want the search feature to perform well under high traffic

**Acceptance Criteria**:

- **Response Time Targets**:

  - Initial search: ≤ 2 seconds (95th percentile)
  - Cached search: ≤ 500ms (95th percentile)
  - Pagination: ≤ 1 second (95th percentile)

- **Caching Strategy**:

  - WordPress transients for frequent queries (TTL: 15 minutes)
  - Redis caching for API responses (TTL: 30 minutes)
  - Browser caching for static assets (plugin JS/CSS)
  - Cache key includes query hash + search parameters

- **Query Optimization**:

  - Database query optimization with proper indexing
  - Vector search result limiting at database level
  - Lazy loading of product images in search results
  - Debounced user input to reduce API calls

- **Resource Management**:
  - Connection pooling for API requests
  - Request queuing to prevent API overload
  - Memory management for large result sets
  - Cleanup of unused cache entries

### Status Flag

`CORE`

### Dependencies & Integrations

- **Infrastructure**: Redis cache server, WordPress transients
- **Monitoring**: Performance metrics collection
- **Database**: Optimized indexes on searchable fields

### Non-functional Requirements

- **Scalability**: Maintains performance with 100+ concurrent users
- **Efficiency**: Minimal server resource consumption
- **Monitoring**: Performance metrics logged for continuous optimization

---

## Future Functionalities (Post-MVP)

### 6. Search Analytics Dashboard

**Status Flag**: `FUTURE`

- Query frequency analysis
- Popular search terms tracking
- Conversion rate by search query
- User behavior flow analysis

### 7. Advanced Filtering & Facets

**Status Flag**: `FUTURE`

- Price range filtering
- Brand and category facets
- Color and size attributes
- Availability status filtering

### 8. Personalized Search Results

**Status Flag**: `FUTURE`

- User search history consideration
- Browsing behavior influence on ranking
- Preference learning from click patterns
- A/B testing for personalization algorithms

### 9. Search Configuration Interface

**Status Flag**: `OPTIONAL`

- Admin panel for weight adjustment
- Search result customization options
- Performance monitoring dashboard
- Cache management tools

### 10. Multi-language Support

**Status Flag**: `FUTURE`

- English language interface option
- Multilingual search query processing
- Localized error messages
- Region-specific result prioritization

---

## Scope Boundary

### Included in MVP

- Hybrid search API endpoint with exact + semantic search
- WordPress plugin with modal interface
- Basic error handling and user feedback
- Performance optimization with caching
- Spanish language support
- Mobile-responsive design

### Explicitly Excluded from MVP

- Shopping cart integration
- User account/authentication features
- Advanced analytics and reporting
- Multi-language support
- Advanced filtering and facets
- Recommendation engine
- Payment processing
- Inventory management integration
- SEO optimization features
- Social sharing capabilities
- Email notifications
- Admin configuration interface (beyond basic API settings)

---

_This functionalities document serves as the definitive specification for all system capabilities and should be referenced throughout the development process to ensure complete requirement coverage._
