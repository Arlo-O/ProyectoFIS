# 📋 Carpeta `app/config/` - Configuración Centralizada

Esta carpeta centraliza toda la **configuración, inicialización y datos de prueba** del proyecto.

## 📁 Contenido

### `settings.py`
**Variables de entorno y configuración global**

- Base de datos (DATABASE_URL, DB_ECHO)
- Ambiente (development, production)
- Credenciales de prueba desde `.env`
- Rutas de directorios (reportes, logs)

**Importar:**
```python
from app.config.settings import DATABASE_URL, IS_DEVELOPMENT
```

---

### `database.py`
**Inicialización de la base de datos**

Funciones:
- `verify_connection()` - Verifica conexión a BD
- `create_tables()` - Crea todas las tablas SQL
- `initialize_database()` - Ejecuta inicialización completa

**Ejecutar una sola vez (después de instalar PostgreSQL):**
```bash
python -c "from app.config.database import initialize_database; initialize_database()"
```

---

### `initial_data.py`
**Insertar datos de prueba iniciales**

Crea:
- Roles del sistema (ADMINISTRADOR, DIRECTOR, PROFESOR, ESTUDIANTE)
- Usuario admin de prueba
- Usuarios de prueba para cada rol

**Ejecutar UNA SOLA VEZ (después de `database.py`):**
```bash
python app/config/initial_data.py
```

Las credenciales de prueba se toman de las variables en `.env`:
- `TEST_ADMIN_EMAIL` / `TEST_ADMIN_PASSWORD`
- `TEST_DIRECTOR_EMAIL` / `TEST_DIRECTOR_PASSWORD`
- `TEST_TEACHER_EMAIL` / `TEST_TEACHER_PASSWORD`
- `TEST_STUDENT_EMAIL` / `TEST_STUDENT_PASSWORD`

---

## 🚀 Workflow de Inicialización Completo

### 1️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar `.env`
```bash
# .env debe tener:
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/fis_db_desarrollo
ENVIRONMENT=development
TEST_ADMIN_EMAIL=admin@colegio.edu
TEST_ADMIN_PASSWORD=admin123
# ... más variables
```

### 3️⃣ Crear tablas en BD
```bash
python -c "from app.config.database import initialize_database; initialize_database()"
```

**Salida esperada:**
```
[✓] Conexión exitosa a la base de datos
[✓] Tablas creadas exitosamente
[✓] BASE DE DATOS INICIALIZADA EXITOSAMENTE
```

### 4️⃣ Insertar datos de prueba
```bash
python app/config/initial_data.py
```

**Salida esperada:**
```
[✓] Rol 'ADMINISTRADOR' creado
[✓] Rol 'DIRECTOR' creado
...
[✓] Admin 'admin@colegio.edu' creado (contraseña: admin123)
```

### 5️⃣ Iniciar la aplicación
```bash
python run_app.py
```

---

## 🔗 Relación con otras carpetas

```
app/
├── config/           ← 📍 Estás aquí (configuración)
│   ├── settings.py   ← Lee .env
│   └── database.py   ← Usa app/data/ para conectar BD
│
├── data/             ← Acceso a BD (ORM, repositories)
├── services/         ← Lógica de negocio
├── ui/               ← Interfaz gráfica
└── core/             ← Modelos
```

**Flujo:**
1. `run_app.py` carga la aplicación
2. `app.data.mappers` se inicializa (usa `app/config/settings.py`)
3. Interfaz UI se crea
4. Usuario hace login
5. `services/` consultan `data/` para obtener datos
6. `data/` usa `settings.py` para conectar a BD

---

## ⚠️ Notas Importantes

- ✅ Los scripts de inicialización (`database.py`, `initial_data.py`) **se ejecutan UNA SOLA VEZ**
- ✅ No elimines archivos de `app/config/` aunque no los uses inmediatamente
- ✅ Para desarrollo, todos los datos de prueba están en `.env`
- ⚠️ **Nunca commitees `.env` a git** (usar `.env.example`)
- ⚠️ En producción, cambiar contraseñas de test y desactivar `DB_ECHO`

---

## 📝 Archivos relacionados en raíz

```
ProyectoFIS/
├── .env                    ← Variables de entorno (NO commitar)
├── .env.example            ← Template de .env (sí commitar)
├── requirements.txt        ← Dependencias Python
├── initialize_db.py        ← DEPRECATED (usar app/config/database.py)
└── run_app.py             ← Entrada principal
```
