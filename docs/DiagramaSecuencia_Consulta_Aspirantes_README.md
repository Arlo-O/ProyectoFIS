# Diagramas de Secuencia: CU-12 - Consultar y Gestionar Aspirantes

## 📋 Descripción

El caso de uso CU-12 se ha dividido en **3 diagramas independientes** para facilitar su compilación en PlantUML Online y mejorar su legibilidad.

## 📁 Archivos

### Parte 1: Navegación y Carga del Módulo
**Archivo:** `DiagramaSecuencia_Consulta_Aspirantes_Parte1.puml`

**Contenido:**
- PASO 1: Directivo hace clic en "Consultar aspirantes"
- PASO 2: Sistema carga dinámicamente el módulo
- Creación de la vista y el servicio
- Estructura básica de la interfaz

**Participantes:** 6 (Directivo, Dashboard, Navegación, Módulo, Vista, Servicio)

**Mensajes:** ~20

---

### Parte 2: Cargar y Mostrar Listado
**Archivo:** `DiagramaSecuencia_Consulta_Aspirantes_Parte2.puml`

**Contenido:**
- PASO 3: Consulta a la base de datos para obtener aspirantes
- Procesamiento de datos (nombre completo, edad, fechas)
- PASO 4: Renderizado de la tabla con Canvas scrollable
- Creación de filas con botones "Ver detalles"

**Participantes:** 5 (Vista, Servicio, Base de Datos, Tabla, Directivo)

**Mensajes:** ~25

**Casos especiales:**
- `alt`: Si no hay aspirantes vs. Si hay aspirantes
- `loop`: Procesamiento de cada aspirante
- `loop`: Creación de cada fila

---

### Parte 3: Ver Detalle de Aspirante
**Archivo:** `DiagramaSecuencia_Consulta_Aspirantes_Parte3.puml`

**Contenido:**
- PASO 5: Directivo hace clic en "Ver detalles"
- PASO 6: Consulta de información completa (aspirante + acudiente)
- PASO 7: Renderizado del detalle completo
- Secciones: Información personal, Acudiente, Acciones disponibles

**Participantes:** 6 (Directivo, Button, Vista, Servicio, DB, Render)

**Mensajes:** ~30

**Casos especiales:**
- `opt`: Consulta y muestra de acudiente (si existe)

---

## 🔗 Flujo Completo

```
Parte 1 → Parte 2 → Parte 3
  ↓         ↓         ↓
Cargar    Listar   Ver Detalle
```

### Secuencia de Eventos

1. **Parte 1**: Directivo → Dashboard → Navegación → Cargar Módulo → Crear Vista
2. **Parte 2**: Consultar BD → Procesar Datos → Renderizar Tabla
3. **Parte 3**: Clic en Detalle → Consultar BD → Renderizar Detalle Completo

---

## 🎨 Cómo Visualizar

### Opción 1: PlantUML Online (Recomendado)

1. Ir a: https://www.plantuml.com/plantuml/uml/
2. Copiar el contenido de cada archivo `.puml`
3. Pegar en el editor
4. Presionar "Submit" o Ctrl+Enter
5. Ver el diagrama generado

**Ventaja:** ✅ Cada parte compila correctamente y se visualiza sin problemas

### Opción 2: VS Code con Extensión

1. Instalar extensión: **PlantUML** (jebbs.plantuml)
2. Abrir cualquier archivo `.puml`
3. Presionar `Alt+D` (Windows/Linux) o `Option+D` (Mac)
4. Ver preview en panel lateral

### Opción 3: Generar Imágenes PNG

```bash
# Para cada parte
java -jar plantuml.jar DiagramaSecuencia_Consulta_Aspirantes_Parte1.puml
java -jar plantuml.jar DiagramaSecuencia_Consulta_Aspirantes_Parte2.puml
java -jar plantuml.jar DiagramaSecuencia_Consulta_Aspirantes_Parte3.puml
```

Genera:
- `DiagramaSecuencia_Consulta_Aspirantes_Parte1.png`
- `DiagramaSecuencia_Consulta_Aspirantes_Parte2.png`
- `DiagramaSecuencia_Consulta_Aspirantes_Parte3.png`

---

## 📊 Comparación con Versión Anterior

| Aspecto | Versión Anterior | Versión Nueva |
|---------|------------------|---------------|
| **Archivos** | 1 archivo | 3 archivos |
| **Líneas** | ~850 líneas | ~200 líneas c/u |
| **Participantes** | 21 | 5-6 por diagrama |
| **Compilación** | ❌ No compila | ✅ Compila correctamente |
| **Legibilidad** | Difícil | Fácil |
| **Mantenimiento** | Complejo | Simple |

---

## 🎯 Beneficios de la Nueva Estructura

### ✅ Compilación Exitosa
- Cada diagrama es independiente y compila sin errores
- Tamaño manejable para PlantUML Online

### ✅ Mejor Legibilidad
- Cada parte se enfoca en un aspecto específico
- Menos elementos por diagrama = más claro

### ✅ Fácil Mantenimiento
- Cambios localizados en cada parte
- No afecta otros diagramas

### ✅ Reutilizable
- Se puede mostrar solo la parte relevante según el contexto
- Ideal para documentación progresiva

---

## 📝 Notas Técnicas

### Simplificaciones Realizadas

1. **Menos auto-llamadas**: Se redujeron las activaciones internas
2. **Nombres más cortos**: "GestionAspirantesView" → "Vista"
3. **Notas concisas**: Solo información esencial
4. **Menos participantes**: Se agruparon elementos relacionados

### Mantenida la Fidelidad

- ✅ Todos los pasos del caso de uso están representados
- ✅ Flujo de datos correcto
- ✅ Consultas a BD documentadas
- ✅ Fragmentos `opt`, `alt`, `loop` donde corresponden

---

## 🔍 Revisión de Contenido

### Parte 1 ✅
- [x] Clic en botón Aspirantes
- [x] Navegación con show_frame
- [x] Carga dinámica del módulo
- [x] Creación de vista y servicio
- [x] Estructura básica de interfaz

### Parte 2 ✅
- [x] Llamada a cargar_listado_aspirantes
- [x] Consulta SQL a base de datos
- [x] Procesamiento de resultados (loop)
- [x] Renderizado de tabla con Canvas
- [x] Creación de filas con botones

### Parte 3 ✅
- [x] Clic en "Ver detalles"
- [x] Ocultar listado, mostrar detalle
- [x] Consulta de aspirante
- [x] Consulta de acudiente (opcional)
- [x] Renderizado de secciones de detalle

---

## 📚 Documentación Relacionada

- `DiagramaSecuencia_Consulta_Aspirantes_Explicado.md` - Documentación detallada original
- `app/services/servicio_aspirante.py` - Implementación del servicio
- `app/ui/modules/aspirantes.py` - Implementación de la vista
- `test_consultar_aspirantes.py` - Tests del caso de uso

---

## ✨ Resultado Final

**3 diagramas modulares, compilables y fáciles de entender que representan fielmente el caso de uso CU-12: Consultar y Gestionar Aspirantes**

---

*Versión 2.0 - Diciembre 2025*  
*División en 3 partes para mejor compilación y legibilidad*
