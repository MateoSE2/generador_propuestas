# System Patterns - AISearch_WorldShishas

## Architectural Patterns

### 1. API Gateway Pattern

**Aplicación**: Endpoint híbrido `/api/v1/hybrid-search/`

- **Responsabilidades**: Orquestación de búsqueda exacta + vectorial
- **Beneficios**: Punto único de entrada, versionado, rate limiting
- **Implementación**: Django REST Framework como gateway

### 2. Composite Search Pattern

**Aplicación**: Combinación de búsquedas exacta + semántica

- **Componentes**:
  - ExactSearchService (MySQL queries)
  - VectorSearchService (Qdrant queries)
  - ResultsMerger (weighted combination)
- **Beneficios**: Mejores resultados que búsquedas individuales
- **Configuración**: Pesos ajustables por tipo de consulta

### 3. Plugin Architecture Pattern

**Aplicación**: WordPress plugin autocontenido

- **Encapsulación**: Estilos, scripts y funcionalidad aislados
- **Distribución**: ZIP instalable independiente
- **Integración**: Hooks WordPress + shortcode opcional

### 4. Progressive Enhancement Pattern

**Aplicación**: Interfaz React con fallback

- **Base**: Funcionalidad básica sin JavaScript
- **Enhancement**: Modal avanzado con React/TypeScript
- **Degradación**: Búsqueda tradicional si falla componente avanzado

### 5. Circuit Breaker Pattern

**Aplicación**: Resiliencia en llamadas API

- **Trigger**: Timeouts o errores repetidos del endpoint híbrido
- **Fallback**: Búsqueda básica WordPress nativa
- **Recovery**: Reintentos gradual tras periodo de enfriamiento

## Integration Patterns

### 6. External Service Integration

**Aplicación**: Comunicación WordPress ↔ byNeural API

- **Protocol**: REST/JSON con autenticación
- **Error Handling**: Timeouts, retry logic, user feedback
- **Caching**: Respuestas frecuentes en WordPress transients

### 7. Event-Driven Updates

**Aplicación**: Sincronización de catálogo (futuro)

- **Triggers**: Cambios en productos WordPress
- **Publishers**: WordPress hooks (save_post, delete_post)
- **Consumers**: byNeural webhooks para reindexado

## Data Patterns

### 8. CQRS (Command Query Responsibility Segregation)

**Aplicación**: Separación lectura/escritura

- **Commands**: Administración productos (WordPress admin)
- **Queries**: Búsqueda híbrida (API optimizada)
- **Beneficios**: Escalabilidad independiente de cada lado

### 9. Result Aggregation Pattern

**Aplicación**: Combinación de múltiples fuentes de búsqueda

- **Sources**: Base de datos relacional + vector store
- **Scoring**: Normalización y weighted merge
- **Pagination**: Cursor-based para consistencia

## UI/UX Patterns

### 10. Modal Overlay Pattern

**Aplicación**: Búsqueda no-intrusiva

- **Trigger**: Click en barra de búsqueda
- **State**: Backdrop blur, focus trap, ESC para cerrar
- **Content**: Progresive disclosure (spinner → resultados → más resultados)

### 11. Infinite Scroll Pattern

**Aplicación**: Carga de resultados adicionales

- **Initial**: 5 resultados principales
- **Expansion**: Botón "Cargar más" para UX controlada
- **Performance**: Lazy loading de imágenes

## Performance Patterns

### 12. Response Caching Pattern

**Aplicación**: Optimización de búsquedas frecuentes

- **Strategy**: TTL-based cache en WordPress
- **Keys**: Hash de query + parámetros de búsqueda
- **Invalidation**: Time-based (15-30 min)

### 13. Asynchronous Processing Pattern

**Aplicación**: Búsquedas no-bloqueantes

- **Frontend**: Promise-based con loading states
- **Backend**: Celery tasks para reindexado (futuro)
- **UX**: Immediate feedback con progressive results

## Security Patterns

### 14. API Authentication Pattern

**Aplicación**: Comunicación segura WordPress ↔ byNeural

- **Method**: API key + request signing
- **Transport**: HTTPS obligatorio
- **Rate Limiting**: Por IP/usuario para prevenir abuse

### 15. Input Sanitization Pattern

**Aplicación**: Validación de consultas de búsqueda

- **Validation**: Longitud máxima, caracteres permitidos
- **Sanitization**: Escape de caracteres especiales
- **Injection Prevention**: Prepared statements en todas las queries
