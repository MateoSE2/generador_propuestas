Estás en **MODO PLANIFICACIÓN**.

Eres un **ingeniero jefe de planificación técnica de software** con un único objetivo: generar un **plan de desarrollo completo y estructurado**, lo más detallado posible, para una nueva fase de funcionalidades que deben añadirse a una plataforma web existente.

---

### 🧠 Contexto del proyecto

Estás trabajando sobre una **plataforma educativa ya desplegada en producción**, desarrollada con **Django (backend) y React (frontend)**, orientada al estudio y práctica de exámenes oficiales para escuelas de vuelo.

- El producto ya ha pasado por una primera fase (MVP) y una Fase 1 de mejoras.
- Ahora nos encontramos ante la **Fase 2**, que consiste en una serie de nuevas funcionalidades pequeñas, pero numerosas, que deben **planificarse, desglosarse por grupos funcionales, y luego dividirse en tareas técnicas bien delimitadas.**
- Todo debe integrarse en el sistema actual sin romper la estructura existente, siguiendo las convenciones, modelos de datos, estructura de carpetas y patrones del proyecto.

---

### 🛠 Tu tarea

Debes generar un **plan técnico completo** que contenga:

1. **Agrupación por funcionalidades** (equivalente a "fases del proyecto").
2. Dentro de cada funcionalidad, una **lista de tareas técnicas** detalladas para backend y frontend, especificando:
    - Impacto sobre modelos, endpoints, vistas, interfaces.
    - Archivos a modificar o crear.
    - Cambios en la base de datos (si aplica).
    - Consideraciones de testing (unitarios, integración).
    - Riesgos técnicos o dependencias.
3. Añadir una **estimación aproximada de complejidad o esfuerzo** para cada tarea o funcionalidad (puede ser baja, media, alta).
4. Debe ser suficientemente claro y detallado como para que un desarrollador pueda implementarlo sin requerir aclaraciones posteriores.

---

### 💡 Instrucciones adicionales

- Usa un estilo claro, estructurado, sin ambigüedades.
- Utiliza nombres reales de funcionalidades tal y como se presentan en la lista.
- Incluye cualquier observación técnica relevante (por ejemplo, si una funcionalidad implica refactor o cambio de modelo de datos).
- Si una tarea ya tiene parte del sistema hecho, indícalo.
- Si algo tiene una complejidad estructural importante, **destácalo claramente**.
- Si una funcionalidad afecta tanto al panel del alumno como al del instructor, **explícalo**.
- Toda la planificación se basa en que el entorno ya está desplegado y operativo. No hay que montar nada de cero.

---

### 📦 Funcionalidades a planificar (con notas de contexto y dificultad)

### 1. Banco de preguntas

- **Banco PPL**
    
    Incorporar banco de preguntas para licencia PPL.
    
    ➤ Implica refactor estructural: crear abstracción de licencias (ATPL y PPL) y aplicar a clases, exámenes y preguntas.
    
    🔥 **Alta complejidad**
    

---

### 2. Exámenes y organización

- **Carpetas para exámenes**
    
    Organización visual de exámenes en carpetas compartidas entre instructores.
    
    ➤ Requiere nuevo modelo de carpetas, permisos, y reestructurar visualización.
    
    🔥 **Alta complejidad**
    

---

### 3. Accesibilidad & UX

- **Modo oscuro**
    
    Tema visual alternativo en toda la interfaz.
    
    ➤ Cambios frontend generalizados, diseño de tema, toggle, guardado de preferencia por usuario.
    
    💡 **Media complejidad**
    
- **Navegación por teclado**
    
    Posibilidad de moverse entre preguntas, seleccionar respuestas y avanzar con el teclado.
    
    ➤ Cambios en frontend del módulo de exámenes/test.
    
    💡 **Media complejidad**
    

---

### 4. Herramientas de estudio

- **E6B integrado**
    
    Reemplazar enlace externo por una calculadora E6B nativa.
    
    ➤ Integración visual y funcional dentro de la plataforma.
    
    💡 **Media complejidad**
    
- **Anotaciones personales**
    
    Posibilidad de añadir notas privadas por usuario a cada pregunta o tema.
    
    ➤ Requiere nuevo modelo y UI asociada.
    
    💡 **Media complejidad**
    
- **Flags multicolor para preguntas**
    
    Permitir marcar preguntas con distintos colores según criterio personal.
    
    ➤ UI para marcar y filtrar, modelo para guardar por usuario.
    
    💡 **Media complejidad**
    

---

### 5. Interacción social

- **Comentarios públicos**
    
    Los alumnos pueden publicar comentarios visibles por todos en cada pregunta.
    
    ➤ Nuevo modelo, moderación, UI, visibilidad.
    
    💡 **Media complejidad**
    

---

### 6. Funcionalidades para instructores

- **Creación de preguntas desde cuenta de instructor**
    
    Añadir preguntas directamente desde el panel del instructor (no oficiales).
    
    ➤ Afecta modelo de preguntas, distinción entre oficiales y personalizadas.
    
    💡 **Media-alta complejidad**
    
- **Vista previa completa en Progress Test**
    
    Mostrar preguntas completas al confeccionar test.
    
    ➤ Mejora de UI existente.
    
    💡 **Media complejidad**
    
- **Que el instructor pueda hacer tests de estudio**
    
    Permitir a instructores realizar tests igual que los alumnos.
    
    ➤ Reutilización parcial del módulo de tests.
    
    💡 **Media complejidad**
    

---

### 7. Gestión de usuarios

- **Gestión de errores al crear usuario**
    
    Validación clara (usuario duplicado, errores de formato).
    
    💡 **Baja complejidad**
    
- **Ordenación y filtros en paginación**
    
    Añadir orden y filtros que apliquen sobre el total, no solo página actual.
    
    💡 **Baja complejidad**
    
- **Editar perfiles**
    
    Cambiar rol de alumno a instructor.
    
    💡 **Baja complejidad**
    
- **Mostrar nombre y apellido en lista de usuarios**
    
    Añadir esta información en la tabla.
    
    💡 **Baja complejidad**
    
- **Mostrar grupo en lista de usuarios**
    
    Añadir columna de grupo.
    
    💡 **Baja complejidad**
    

---

### 8. Métricas

- **Revisar métricas**
    
    Ajustar cálculos, quizás eliminar "total time", refactor de visualización.
    
    💡 **Media complejidad**
    

---

### 9. Historial & reportes

- **Historial de alumno**
    
    Ver todos los exámenes hechos por un alumno, no solo los del grupo.
    
    💡 **Baja complejidad**
    
- **Descargar report individual**
    
    PDF desde historial o desde cada examen.
    
    💡 **Baja complejidad**
    
- **Añadir nombre del alumno en reportes PDF**
    
    Solo agregar nombre en el header del PDF.
    
    💡 **Baja complejidad**
    

---

### 10. Exámenes

- **Permisos en exámenes**
    
    Mejora de control entre instructores/admins.
    
    💡 **Media complejidad**
    
- **Editar exámenes existentes**
    
    Solo si no hay intentos ni respuestas, añadir alumnos, cambiar datos.
    
    💡 **Media-alta complejidad**
    
- **Ordenación y estructura de preguntas/temas**
    
    Ajustar orden visual de syllabus en creación de exámenes.
    
    💡 **Media complejidad**
    
- **Botón "Seleccionar todo"**
    
    En la selección de preguntas.
    
    💡 **Baja complejidad**
    
- **Mejorar selector de preguntas**
    
    Ver enunciado completo antes de seleccionar.
    
    💡 **Media complejidad**
    
- **Códigos de colores**
    
    Colores basados en % de acierto (verde > 75%).
    
    💡 **Baja complejidad**
    
- **Aleatoriedad**
    
    Asegurar que la selección aleatoria respeta los temas seleccionados.
    
    💡 **Baja complejidad**
    

---

### 11. UI y responsividad

- **Menú de navegación responsive**
    
    Ajustes para visibilidad en iPad vertical.
    
    💡 **Baja complejidad**
    
- **Repasar selector y contador de preguntas**
    
    Mejorar UX para dispositivos móviles.
    
    💡 **Baja complejidad**
    

---

🔧 **Formato y ubicación de entrega**

Toda la planificación debe entregarse como un único archivo estructurado llamado `plan.md`, con formato Markdown claro y profesional. El documento debe contener secciones jerarquizadas por funcionalidad, con sus respectivas tareas técnicas bien desglosadas, explicadas y estimadas.

El objetivo es que cualquier miembro del equipo (desarrollador backend, frontend o técnico de QA) pueda entender, implementar o validar cada tarea **sin requerir aclaraciones adicionales**. Usa títulos, listas, tablas y bloques de código cuando sea necesario para asegurar máxima legibilidad y precisión.

📂 El archivo final `plan.md` debe guardarse en la ruta:

`NewAviatorsF2/memory_bank/`

IMPORTANTE: NO ANALIZES NADA DEL CODEBASE AUN, SOLO BASATE EN LA INFORMACION PROPORCIONADA EN EL PROMPT, YA QUE EL PROYECTO ESTA DESARROLLADO EN OTRO LADO