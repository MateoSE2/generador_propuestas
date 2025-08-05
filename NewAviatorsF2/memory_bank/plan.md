# Plan Técnico - Fase 2: Funcionalidades Avanzadas
## Plataforma Educativa de Aviación

---

## 📋 Resumen Ejecutivo

Este documento presenta el plan técnico completo para la **Fase 2** de la plataforma educativa de aviación, construida sobre Django (backend) y React (frontend). La fase contempla **39 tareas técnicas** distribuidas en **11 grupos funcionales**, desde refactors estructurales hasta mejoras de UX/UI.

**Alcance total estimado:** 320-450 horas de desarrollo
**Funcionalidades:** 31 características nuevas
**Complejidad general:** Media-Alta debido a refactors estructurales

---

## 🏗️ Grupos Funcionales por Complejidad

### 🔥 GRUPO 1: REFACTORS ESTRUCTURALES (Alta Complejidad)

#### 1.1 Banco de Preguntas PPL
**Complejidad:** 🔥 Alta | **Estimación:** 60-80 horas

**Descripción:** Incorporar banco de preguntas para licencia PPL, requiriendo abstracción completa del sistema de licencias.

**Tareas Backend:**
- **Tarea 1.1.1:** Crear abstracción de licencias
  - Refactorizar modelo `License` para soportar ATPL y PPL
  - Migración de datos existentes manteniendo integridad
  - Archivos afectados: `models.py`, migraciones
  - Testing: Unitarios para modelo, integridad de datos

- **Tarea 1.1.2:** Adaptar modelo de preguntas
  - Añadir campo `license_type` a modelo `Question`
  - Crear relación Many-to-Many con licencias
  - Archivos afectados: `models.py`, `serializers.py`
  - Testing: Validación de integridad referencial

- **Tarea 1.1.3:** Endpoints específicos por licencia
  - Crear endpoints filtrados por tipo de licencia
  - Modificar serializers existentes
  - Archivos afectados: `views.py`, `urls.py`, `serializers.py`
  - Testing: Integración de endpoints, permisos

**Tareas Frontend:**
- **Tarea 1.1.4:** Selector de licencia en navegación
  - Componente global para cambio de contexto
  - Estado global para licencia activa
  - Archivos afectados: `App.js`, `LicenseContext.js`, components globales
  - Testing: Componente, estado global

- **Tarea 1.1.5:** Filtrado dinámico en interfaces
  - Adaptar listados de preguntas, exámenes, estadísticas
  - Modificar servicios API existentes
  - Archivos afectados: Services, componentes de listado
  - Testing: Integración con API, UI

**Riesgos técnicos:**
- Migración de datos sin pérdida de información
- Impacto en rendimiento por filtrado adicional
- Compatibilidad con sistema de permisos existente

---

#### 1.2 Carpetas para Exámenes
**Complejidad:** 🔥 Alta | **Estimación:** 50-70 horas

**Descripción:** Sistema de organización visual de exámenes en carpetas compartidas entre instructores.

**Tareas Backend:**
- **Tarea 1.2.1:** Modelo de carpetas
  - Crear modelo `ExamFolder` con jerarquía
  - Relaciones con exámenes e instructores
  - Archivos afectados: `models.py`, migraciones
  - Testing: Jerarquía, permisos, integridad

- **Tarea 1.2.2:** Sistema de permisos para carpetas
  - Herencia de permisos padre-hijo
  - Compartir carpetas entre instructores
  - Archivos afectados: `permissions.py`, `views.py`
  - Testing: Casos edge de permisos, herencia

- **Tarea 1.2.3:** Endpoints de gestión
  - CRUD completo para carpetas
  - Mover exámenes entre carpetas
  - Archivos afectados: `views.py`, `serializers.py`, `urls.py`
  - Testing: Operaciones CRUD, validaciones

**Tareas Frontend:**
- **Tarea 1.2.4:** Interfaz de carpetas tipo árbol
  - Componente navegable con drag & drop
  - Vista jerárquica expandible/colapsable
  - Archivos afectados: `FolderTree.js`, CSS específico
  - Testing: Interacción, drag & drop, performance

- **Tarea 1.2.5:** Gestión de carpetas
  - Crear, editar, eliminar carpetas
  - Modal de permisos y compartir
  - Archivos afectados: `FolderManager.js`, modales relacionados
  - Testing: CRUD operations, validaciones UI

**Riesgos técnicos:**
- Complejidad de permisos anidados
- Performance con muchas carpetas/exámenes
- UX intuitiva para organización

---

### 💪 GRUPO 2: FUNCIONALIDADES CORE (Media-Alta Complejidad)

#### 2.1 Creación de Preguntas por Instructores
**Complejidad:** 💪 Media-Alta | **Estimación:** 40-55 horas

**Tareas Backend:**
- **Tarea 2.1.1:** Distinción preguntas oficiales/personalizadas
  - Campo `is_official` en modelo Question
  - Filtros por tipo en queries
  - Archivos afectados: `models.py`, `views.py`, migraciones
  - Testing: Segregación de datos, permisos

- **Tarea 2.1.2:** Endpoints para instructores
  - CRUD completo para preguntas personalizadas
  - Validaciones específicas para instructores
  - Archivos afectados: `instructor_views.py`, `serializers.py`
  - Testing: Permisos, validaciones, integridad

**Tareas Frontend:**
- **Tarea 2.1.3:** Editor de preguntas
  - Formulario completo con validaciones
  - Preview en tiempo real
  - Archivos afectados: `QuestionEditor.js`, `QuestionPreview.js`
  - Testing: Formulario, validaciones, preview

- **Tarea 2.1.4:** Gestión de preguntas del instructor
  - Lista, editar, eliminar preguntas propias
  - Filtros y búsqueda
  - Archivos afectados: `InstructorQuestions.js`
  - Testing: CRUD, filtros, paginación

---

#### 2.2 Editar Exámenes Existentes
**Complejidad:** 💪 Media-Alta | **Estimación:** 35-50 horas

**Tareas Backend:**
- **Tarea 2.2.1:** Validaciones de edición
  - Verificar ausencia de intentos/respuestas
  - Estados de examen (draft, active, completed)
  - Archivos afectados: `models.py`, `validators.py`
  - Testing: Edge cases, validaciones

- **Tarea 2.2.2:** Endpoints de edición
  - Modificar datos básicos del examen
  - Añadir/quitar alumnos si cumple condiciones
  - Archivos afectados: `exam_views.py`
  - Testing: Condiciones de edición, permisos

**Tareas Frontend:**
- **Tarea 2.2.3:** Interfaz de edición
  - Formulario con validaciones contextuales
  - Warnings sobre limitaciones
  - Archivos afectados: `ExamEditor.js`
  - Testing: Validaciones UI, feedback

---

### 🎨 GRUPO 3: MEJORAS UX/UI (Media Complejidad)

#### 3.1 Modo Oscuro
**Complejidad:** 💡 Media | **Estimación:** 25-35 horas

**Tareas Frontend:**
- **Tarea 3.1.1:** Sistema de temas
  - Definir variables CSS para tema claro/oscuro
  - Toggle component reutilizable
  - Archivos afectados: `themes.css`, `ThemeToggle.js`
  - Testing: Cambio de tema, persistencia

- **Tarea 3.1.2:** Aplicar tema a toda la aplicación
  - Revisar y adaptar todos los componentes
  - Verificar contraste y accesibilidad
  - Archivos afectados: Todos los CSS/styled-components
  - Testing: Visual regression, accesibilidad

**Tareas Backend:**
- **Tarea 3.1.3:** Preferencia de usuario
  - Campo `theme_preference` en perfil
  - Endpoint para guardar preferencia
  - Archivos afectados: `User model`, `profile_views.py`
  - Testing: Persistencia, API

---

#### 3.2 Navegación por Teclado
**Complejidad:** 💡 Media | **Estimación:** 20-30 horas

**Tareas Frontend:**
- **Tarea 3.2.1:** Atajos en módulo de exámenes
  - Navegación entre preguntas (←→)
  - Selección de respuestas (1,2,3,4)
  - Submit y navegación (Enter, Space)
  - Archivos afectados: `ExamInterface.js`, `QuestionComponent.js`
  - Testing: Eventos teclado, accesibilidad

- **Tarea 3.2.2:** Indicadores visuales
  - Mostrar atajos disponibles
  - Feedback visual de navegación
  - Archivos afectados: `KeyboardHints.js`
  - Testing: Visibilidad, UX

---

#### 3.3 E6B Integrado
**Complejidad:** 💡 Media | **Estimación:** 30-40 horas

**Tareas Frontend:**
- **Tarea 3.3.1:** Calculadora E6B nativa
  - Implementar funciones de cálculo aeronáutico
  - Interfaz visual similar a E6B físico
  - Archivos afectados: `E6BCalculator.js`, cálculos específicos
  - Testing: Precisión de cálculos, UI

- **Tarea 3.3.2:** Integración en plataforma
  - Modal/sidebar accesible desde exámenes
  - Persistir estado durante uso
  - Archivos afectados: `ExamLayout.js`
  - Testing: Integración, persistencia estado

---

#### 3.4 Herramientas de Estudio

##### 3.4.1 Anotaciones Personales
**Complejidad:** 💡 Media | **Estimación:** 25-35 horas

**Tareas Backend:**
- **Tarea 3.4.1.1:** Modelo de anotaciones
  - Relación Usuario-Pregunta-Nota
  - Texto rico opcional
  - Archivos afectados: `models.py`, migraciones
  - Testing: Relaciones, validaciones

- **Tarea 3.4.1.2:** Endpoints de anotaciones
  - CRUD para notas personales
  - Archivos afectados: `notes_views.py`
  - Testing: Permisos, CRUD

**Tareas Frontend:**
- **Tarea 3.4.1.3:** Editor de notas
  - Componente para añadir/editar notas
  - Rich text editor básico
  - Archivos afectados: `NoteEditor.js`
  - Testing: Editor, persistencia

##### 3.4.2 Flags Multicolor
**Complejidad:** 💡 Media | **Estimación:** 20-25 horas

**Tareas Backend:**
- **Tarea 3.4.2.1:** Modelo de flags
  - Usuario-Pregunta-Color
  - Preset de colores disponibles
  - Archivos afectados: `models.py`
  - Testing: Relaciones, colores válidos

**Tareas Frontend:**
- **Tarea 3.4.2.2:** Sistema de marcado
  - Selector de colores en preguntas
  - Filtros por color en listados
  - Archivos afectados: `QuestionFlag.js`, `ColorPicker.js`
  - Testing: Marcado, filtros

---

### 👥 GRUPO 4: INTERACCIÓN SOCIAL (Media Complejidad)

#### 4.1 Comentarios Públicos
**Complejidad:** 💡 Media | **Estimación:** 30-40 horas

**Tareas Backend:**
- **Tarea 4.1.1:** Modelo de comentarios
  - Usuario-Pregunta-Comentario
  - Sistema básico de moderación
  - Archivos afectados: `models.py`, migraciones
  - Testing: Relaciones, moderación

- **Tarea 4.1.2:** Endpoints y moderación
  - CRUD para comentarios
  - Endpoints para moderadores
  - Archivos afectados: `comments_views.py`
  - Testing: Permisos, moderación

**Tareas Frontend:**
- **Tarea 4.1.3:** Interfaz de comentarios
  - Lista de comentarios por pregunta
  - Formulario de nuevo comentario
  - Archivos afectados: `Comments.js`, `CommentForm.js`
  - Testing: CRUD, actualización tiempo real

- **Tarea 4.1.4:** Panel de moderación
  - Lista de comentarios reportados
  - Acciones de moderación
  - Archivos afectados: `ModerationPanel.js`
  - Testing: Permisos moderador, acciones

---

### 👨‍🏫 GRUPO 5: FUNCIONALIDADES PARA INSTRUCTORES (Media Complejidad)

#### 5.1 Vista Previa Completa en Progress Test
**Complejidad:** 💡 Media | **Estimación:** 15-20 horas

**Tareas Frontend:**
- **Tarea 5.1.1:** Mejorar UI de selección
  - Mostrar enunciado completo en selector
  - Preview expandible de preguntas
  - Archivos afectados: `QuestionSelector.js`
  - Testing: UI, performance con muchas preguntas

---

#### 5.2 Instructores Realizando Tests
**Complejidad:** 💡 Media | **Estimación:** 20-25 horas

**Tareas Backend:**
- **Tarea 5.2.1:** Permisos para instructores
  - Modificar lógica de acceso a tests
  - Rol mixto alumno-instructor
  - Archivos afectados: `permissions.py`, `test_views.py`
  - Testing: Permisos, roles

**Tareas Frontend:**
- **Tarea 5.2.2:** Interfaz unificada
  - Reutilizar componentes de test de alumnos
  - Adaptaciones menores para instructores
  - Archivos afectados: `TestInterface.js`
  - Testing: Reutilización componentes

---

### 👤 GRUPO 6: GESTIÓN DE USUARIOS (Baja Complejidad)

#### 6.1 Gestión de Errores al Crear Usuario
**Complejidad:** 💚 Baja | **Estimación:** 8-12 horas

**Tareas Backend:**
- **Tarea 6.1.1:** Validaciones mejoradas
  - Validar email duplicado
  - Mensajes de error específicos
  - Archivos afectados: `serializers.py`, `validators.py`
  - Testing: Validaciones, mensajes error

**Tareas Frontend:**
- **Tarea 6.1.2:** Feedback de errores
  - Mostrar errores específicos en formulario
  - Archivos afectados: `UserForm.js`
  - Testing: Display errores, UX

---

#### 6.2 Ordenación y Filtros en Paginación
**Complejidad:** 💚 Baja | **Estimación:** 12-15 horas

**Tareas Backend:**
- **Tarea 6.2.1:** Ordenación global
  - Implementar ordenación antes de paginar
  - Filtros que apliquen al queryset completo
  - Archivos afectados: `views.py`, `filters.py`
  - Testing: Ordenación, filtros, paginación

**Tareas Frontend:**
- **Tarea 6.2.2:** Controles de ordenación
  - Headers clickeables para ordenar
  - Indicadores visuales de orden actual
  - Archivos afectados: `UserTable.js`
  - Testing: Interacción ordenación

---

#### 6.3 Editar Perfiles
**Complejidad:** 💚 Baja | **Estimación:** 10-15 horas

**Tareas Backend:**
- **Tarea 6.3.1:** Cambio de rol
  - Endpoint para modificar rol usuario
  - Validaciones de permisos
  - Archivos afectados: `user_views.py`
  - Testing: Cambio rol, permisos

**Tareas Frontend:**
- **Tarea 6.3.2:** Interfaz edición perfil
  - Formulario con selector de rol
  - Archivos afectados: `ProfileEditor.js`
  - Testing: Formulario, validaciones

---

#### 6.4 Mostrar Información Adicional en Lista
**Complejidad:** 💚 Baja | **Estimación:** 6-10 horas

**Tareas Backend:**
- **Tarea 6.4.1:** Serializer ampliado
  - Incluir nombre, apellido, grupo en listado
  - Archivos afectados: `serializers.py`
  - Testing: Datos en respuesta

**Tareas Frontend:**
- **Tarea 6.4.2:** Columnas adicionales
  - Mostrar nueva información en tabla
  - Archivos afectados: `UserTable.js`
  - Testing: Display información

---

### 📊 GRUPO 7: MÉTRICAS Y REPORTES (Media Complejidad)

#### 7.1 Revisar Métricas
**Complejidad:** 💡 Media | **Estimación:** 20-30 horas

**Tareas Backend:**
- **Tarea 7.1.1:** Refactor cálculos
  - Revisar lógica de "total time"
  - Optimizar queries de métricas
  - Archivos afectados: `metrics.py`, `views.py`
  - Testing: Precisión de cálculos

**Tareas Frontend:**
- **Tarea 7.1.2:** Visualización mejorada
  - Componentes de métricas más claros
  - Archivos afectados: `MetricsDisplay.js`
  - Testing: Visualización, precisión datos

---

### 📋 GRUPO 8: HISTORIAL Y REPORTES (Baja Complejidad)

#### 8.1 Historial Completo de Alumno
**Complejidad:** 💚 Baja | **Estimación:** 8-12 horas

**Tareas Backend:**
- **Tarea 8.1.1:** Query ampliado
  - Incluir exámenes de todos los grupos
  - Archivos afectados: `student_views.py`
  - Testing: Datos completos

---

#### 8.2 Reportes PDF Mejorados
**Complejidad:** 💚 Baja | **Estimación:** 12-18 horas

**Tareas Backend:**
- **Tarea 8.2.1:** PDF con nombre alumno
  - Añadir nombre en header del PDF
  - Endpoint para descarga individual
  - Archivos afectados: `pdf_generator.py`, `report_views.py`
  - Testing: Generación PDF, datos correctos

---

### 📝 GRUPO 9: MEJORAS EN EXÁMENES (Baja-Media Complejidad)

#### 9.1 Permisos en Exámenes
**Complejidad:** 💡 Media | **Estimación:** 15-20 horas

**Tareas Backend:**
- **Tarea 9.1.1:** Sistema de permisos refinado
  - Distinguir entre instructor y admin
  - Archivos afectados: `permissions.py`
  - Testing: Permisos por rol

---

#### 9.2 Mejoras en Selector de Preguntas
**Complejidad:** 💡 Media | **Estimación:** 18-25 horas

**Tareas Frontend:**
- **Tarea 9.2.1:** Botón "Seleccionar todo"
  - Implementar selección masiva
  - Archivos afectados: `QuestionSelector.js`
  - Testing: Selección masiva

- **Tarea 9.2.2:** Vista previa mejorada
  - Enunciado completo antes de seleccionar
  - Archivos afectados: `QuestionPreview.js`
  - Testing: Preview, performance

---

#### 9.3 Códigos de Colores y Aleatoriedad
**Complejidad:** 💚 Baja | **Estimación:** 10-15 horas

**Tareas Frontend:**
- **Tarea 9.3.1:** Colores por % acierto
  - Verde >75%, amarillo 50-75%, rojo <50%
  - Archivos afectados: `QuestionStatus.js`
  - Testing: Lógica colores

**Tareas Backend:**
- **Tarea 9.3.2:** Aleatoriedad mejorada
  - Asegurar respeto a temas seleccionados
  - Archivos afectados: `exam_generator.py`
  - Testing: Distribución aleatoria

---

#### 9.4 Ordenación de Syllabus
**Complejidad:** 💡 Media | **Estimación:** 12-18 horas

**Tareas Backend:**
- **Tarea 9.4.1:** Orden configurable
  - Campo `order` en modelo Topic/Theme
  - Archivos afectados: `models.py`
  - Testing: Ordenación

**Tareas Frontend:**
- **Tarea 9.4.2:** Interfaz de ordenación
  - Drag & drop para reordenar temas
  - Archivos afectados: `TopicOrganizer.js`
  - Testing: Drag & drop, persistencia

---

### 📱 GRUPO 10: RESPONSIVE Y UI (Baja Complejidad)

#### 10.1 Menú Responsive
**Complejidad:** 💚 Baja | **Estimación:** 8-12 horas

**Tareas Frontend:**
- **Tarea 10.1.1:** Ajustes iPad vertical
  - Media queries específicas
  - Archivos afectados: `Navigation.css`
  - Testing: Responsive en iPad

---

#### 10.2 Selector y Contador Mobile
**Complejidad:** 💚 Baja | **Estimación:** 10-15 horas

**Tareas Frontend:**
- **Tarea 10.2.1:** UX mobile mejorada
  - Componentes optimizados para móvil
  - Archivos afectados: `QuestionCounter.js`, `QuestionSelector.js`
  - Testing: UX móvil

---

## 📊 Resumen de Estimaciones

### Por Complejidad
- **🔥 Alta:** 110-150 horas (2 funcionalidades)
- **💪 Media-Alta:** 75-105 horas (2 funcionalidades)  
- **💡 Media:** 135-195 horas (21 funcionalidades)
- **💚 Baja:** 84-127 horas (6 funcionalidades)

### Por Grupo Funcional
1. **Refactors Estructurales:** 110-150h
2. **Funcionalidades Core:** 75-105h
3. **Mejoras UX/UI:** 120-165h
4. **Interacción Social:** 30-40h
5. **Funcionalidades Instructores:** 35-45h
6. **Gestión Usuarios:** 36-52h
7. **Métricas:** 20-30h
8. **Reportes:** 20-30h
9. **Mejoras Exámenes:** 55-78h
10. **Responsive:** 18-27h

**TOTAL ESTIMADO: 519-722 horas**

---

## 🚨 Riesgos Técnicos Principales

### Alto Riesgo
1. **Migración de datos** en refactor de licencias
2. **Performance** con sistema de carpetas jerárquicas
3. **Compatibilidad** con sistema de permisos existente

### Riesgo Medio
1. **Complejidad de permisos** anidados en carpetas
2. **Estados concurrentes** en edición de exámenes
3. **Integración** de modo oscuro sin romper componentes

### Riesgo Bajo
1. **Regresiones visuales** en cambios de UI
2. **Performance** en dispositivos móviles
3. **Compatibilidad** entre navegadores

---

## 🎯 Dependencias Críticas

### Secuenciales (Deben completarse en orden)
1. **Banco PPL** → Todas las funcionalidades que usen preguntas
2. **Carpetas** → Gestión avanzada de exámenes
3. **Modo oscuro** → Todas las mejoras visuales posteriores

### Paralelas (Pueden desarrollarse simultáneamente)
- Herramientas de estudio (anotaciones, flags)
- Mejoras de gestión de usuarios
- Sistema de comentarios
- Reportes y métricas

---

## 📋 Plan de Testing

### Testing por Fase
1. **Unitario:** Cada modelo y función nueva
2. **Integración:** APIs y componentes complejos
3. **E2E:** Flujos críticos (crear examen, realizar test)
4. **Visual:** Regresión en cambios de UI
5. **Performance:** Consultas complejas y componentes pesados

### Cobertura Mínima
- **Backend:** 85% cobertura en funcionalidades nuevas
- **Frontend:** Testing de componentes críticos
- **E2E:** Flujos principales de usuario

---

## 🚀 Recomendaciones de Implementación

### Fase 1 (Crítica - 2-3 meses)
- Banco PPL (refactor estructural)
- Carpetas para exámenes
- Modo oscuro básico

### Fase 2 (Core - 1-2 meses)  
- Creación de preguntas por instructores
- Herramientas de estudio (anotaciones, flags)
- Mejoras en gestión de usuarios

### Fase 3 (Mejoras - 1-2 meses)
- E6B integrado
- Comentarios públicos
- Navegación por teclado
- Mejoras en exámenes

### Fase 4 (Pulido - 1 mes)
- Responsive final
- Métricas optimizadas
- Reportes mejorados
- Testing exhaustivo

---

*Documento generado para Fase 2 - Plataforma Educativa de Aviación*
*Última actualización: [Fecha actual]*