# 🗂️ Plan de Reorganización del Proyecto

## 📊 Estado Actual vs Propuesto

### Archivos a MOVER:

```
# MOVER seed_permisos.py a scripts/
seed_permisos.py  →  scripts/seed_permisos.py

# MOVER archivos de testing
test_scroll_form.py  →  tests/test_scroll_form.py
(crear carpeta tests/ si no existe)

# MOVER documentación
SOLUCION_COMPLETA.md  →  docs/SOLUCION_COMPLETA.md
```

### Archivos a ELIMINAR:

```
❌ demo_error_counter.py  (código de prueba temporal)
```

### Archivos a REVISAR:

```
⚠️ initialize_db.py - Comparar con scripts/clean_database.sql
   → Si hace lo mismo, eliminar
   → Si es diferente, mover a scripts/
```

---

## 📁 Estructura Propuesta Final

```
ProyectoFIS/
├── .env                          ✅ Variables de entorno
├── requirements.txt              ✅ Dependencias
├── run_app.py                    ✅ Punto de entrada
├── run_tests.py                  ✅ Ejecutor de tests
├── 
├── app/                          ✅ Código de la aplicación
├── scripts/                      ✅ Scripts de BD y mantenimiento
│   ├── clean_database.sql
│   ├── create_test_users.py
│   ├── reiniciar_bd_completa.py
│   └── seed_permisos.py         📦 MOVER AQUÍ
├── 
├── tests/                        📦 CREAR esta carpeta
│   └── test_scroll_form.py      📦 MOVER AQUÍ
├── 
├── docs/                         ✅ Documentación
│   ├── DiagramaSecuencia_CU02_CU04.puml
│   └── SOLUCION_COMPLETA.md     📦 MOVER AQUÍ
├── 
├── backup_pre_cleanup/           ✅ Backups (mantener)
├── reportes/                     ✅ Carpeta de reportes generados
└── venvFIS/                      ✅ Entorno virtual
```

---

## 🎯 Clasificación de Archivos

### 🟢 ESENCIALES (No tocar):
- `.env`
- `requirements.txt`
- `run_app.py`
- `run_tests.py`
- `app/` (toda la carpeta)
- `scripts/` (toda la carpeta)

### 🟡 REORGANIZAR:
- `seed_permisos.py` → `scripts/seed_permisos.py`
- `test_scroll_form.py` → `tests/test_scroll_form.py`
- `SOLUCION_COMPLETA.md` → `docs/SOLUCION_COMPLETA.md`

### 🔴 ELIMINAR:
- `demo_error_counter.py`

### ⚠️ REVISAR:
- `initialize_db.py` (¿duplica funcionalidad?)

---

## ✅ Comandos para Reorganizar

```powershell
# 1. Crear carpeta tests si no existe
New-Item -ItemType Directory -Force -Path tests

# 2. Mover archivos
Move-Item seed_permisos.py scripts/seed_permisos.py
Move-Item test_scroll_form.py tests/test_scroll_form.py
Move-Item SOLUCION_COMPLETA.md docs/SOLUCION_COMPLETA.md

# 3. Eliminar archivos temporales
Remove-Item demo_error_counter.py

# 4. REVISAR initialize_db.py antes de eliminar
# (comparar con scripts/clean_database.sql y scripts/reiniciar_bd_completa.py)
```

---

## 📝 Después de Reorganizar

### Actualizar referencias en código:

1. **Si mueves seed_permisos.py a scripts/:**
   - Actualizar `scripts/reiniciar_bd_completa.py` línea 87:
     ```python
     # DE:
     resultado = subprocess.run([sys.executable, "seed_permisos.py"], ...)
     
     # A:
     resultado = subprocess.run([sys.executable, "scripts/seed_permisos.py"], ...)
     ```

2. **Actualizar documentación:**
   - Actualizar referencias en README (si existe)
   - Actualizar SOLUCION_COMPLETA.md con nuevas rutas

---

## 🚀 Resultado Final

Después de la reorganización, la raíz del proyecto tendrá solo:
- Archivos de configuración (`.env`, `requirements.txt`)
- Puntos de entrada (`run_app.py`, `run_tests.py`)
- Carpetas organizadas (`app/`, `scripts/`, `tests/`, `docs/`)

**Proyecto más limpio, más profesional, más fácil de mantener.**
