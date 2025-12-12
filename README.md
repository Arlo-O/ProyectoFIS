# 🎓 Sistema de Gestión Académica FIS

Sistema integral para la gestión académica de una institución educativa, desarrollado con Python, SQLAlchemy y Tkinter.

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
- [Usuarios de Prueba](#usuarios-de-prueba)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Control de Versiones](#control-de-versiones)
- [Arquitectura](#arquitectura)

---

## 🔧 Requisitos Previos

### Software Necesario

- **Python 3.10+** ([Descargar](https://www.python.org/downloads/))
- **PostgreSQL 14+** ([Descargar](https://www.postgresql.org/download/))
- **pgAdmin 4** (incluido con PostgreSQL)
- **Git** ([Descargar](https://git-scm.com/downloads))

### Base de Datos PostgreSQL

Antes de comenzar, debes tener PostgreSQL instalado y configurado con:

- **Usuario:** `fis_user`
- **Contraseña:** `fis_password`
- **Base de datos:** `fis_db_desarrollo`

**Comandos para crear la BD en PostgreSQL:**

```sql
-- En psql o pgAdmin:
CREATE USER fis_user WITH PASSWORD 'fis_password';
CREATE DATABASE fis_db_desarrollo OWNER fis_user;
GRANT ALL PRIVILEGES ON DATABASE fis_db_desarrollo TO fis_user;
```

---

## 📦 Instalación

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd ProyectoFIS
```

### 2. Crear Entorno Virtual

**En Windows (PowerShell):**

```powershell
python -m venv venvFIS
.\venvFIS\Scripts\Activate.ps1
```

**En Linux/Mac:**

```bash
python3 -m venv venvFIS
source venvFIS/bin/activate
```

### 3. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Verifica que el archivo `.env` en la raíz del proyecto contenga:

```env
DATABASE_URL=postgresql+psycopg2://fis_user:fis_password@localhost:5432/fis_db_desarrollo
SECRET_KEY=tu_clave_secreta_aqui
```

---

## 🗄️ Configuración de la Base de Datos

### Orden de Ejecución (IMPORTANTE)

Sigue estos pasos **EN ORDEN** para inicializar la base de datos:

#### **Paso 1: Limpiar y Recrear la Base de Datos**

Abre **pgAdmin**, conéctate a `fis_db_desarrollo` y ejecuta el script:

```
scripts/clean_database.sql
```

Este script:
- ✅ Elimina todos los datos existentes
- ✅ Elimina todas las tablas
- ✅ Reinicia las secuencias
- ✅ Recrea las 28 tablas del sistema
- ✅ Inserta los 5 roles base
- ✅ Otorga permisos al usuario `fis_user`

#### **Paso 2: Ejecutar Script de Reinicio Completo**

En la terminal con el entorno virtual activado:

```powershell
python scripts/reiniciar_bd_completa.py
```

Este script:
1. Te pedirá confirmar que ejecutaste el Paso 1 ✅
2. Ejecuta `scripts/create_test_users.py` - Crea 4 usuarios de prueba
3. Ejecuta `scripts/seed_permisos.py` - Crea 27 permisos y los asigna a roles

**Alternativa Manual:**

Si prefieres ejecutar los scripts por separado:

```powershell
# Después de ejecutar clean_database.sql en pgAdmin:
python scripts/create_test_users.py
python scripts/seed_permisos.py
```

---

## 🚀 Ejecución del Proyecto

Una vez configurada la base de datos, ejecuta:

```powershell
python run_app.py
```

Se abrirá la ventana de login de la aplicación.

---

## 👥 Usuarios de Prueba

Después de ejecutar los scripts de inicialización, puedes usar:

| Correo Electrónico      | Contraseña   | Rol            | Permisos                          |
|------------------------|--------------|----------------|-----------------------------------|
| `admin@colegio.edu`    | `admin123`   | Administrador  | Acceso total al sistema          |
| `director@colegio.edu` | `dir123`     | Director       | Gestión académica y reportes     |
| `profesor@colegio.edu` | `prof123`    | Profesor       | Calificaciones y anotaciones     |
| `padre@colegio.edu`    | `papa123`    | Acudiente      | Ver desempeño del estudiante     |

---

## 📁 Estructura del Proyecto

```
ProyectoFIS/
│
├── app/                        # Código principal de la aplicación
│   ├── core/                   # Modelos de dominio (entidades)
│   │   ├── academico/          # Grado, Grupo, HojaVida, etc.
│   │   ├── gestion/            # Citación, Entrevista, etc.
│   │   ├── logros/             # Logros, Evaluaciones, Boletines
│   │   └── usuarios/           # Usuario, Rol, Permiso, Persona, etc.
│   │
│   ├── data/                   # Capa de datos
│   │   ├── db.py               # Configuración de SQLAlchemy
│   │   ├── mappers.py          # Mapeo ORM (28 tablas)
│   │   ├── repositories.py     # Repositorios para acceso a datos
│   │   └── uow.py              # Unit of Work pattern
│   │
│   ├── services/               # Lógica de negocio
│   │   ├── auth_service.py     # Autenticación y autorización
│   │   ├── rbac_service.py     # Control de acceso basado en roles
│   │   └── ...                 # Otros servicios
│   │
│   └── ui/                     # Interfaz gráfica (Tkinter)
│       ├── main.py             # Punto de entrada de la GUI
│       ├── components/         # Componentes reutilizables
│       └── modules/            # Módulos por rol (admin, director, etc.)
│
├── scripts/                    # Scripts de base de datos
│   ├── clean_database.sql      # Recrea toda la estructura
│   ├── create_test_users.py    # Crea usuarios de prueba
│   ├── seed_permisos.py        # Carga permisos
│   └── reiniciar_bd_completa.py # Script todo-en-uno
│
├── docs/                       # Documentación
│   └── CU-03_Crear_Usuario.md  # Documentación del flujo de creación de usuarios
│
├── logs/                       # Logs del sistema (NO subir a Git)
│   └── credenciales_usuarios.txt # Log de contraseñas generadas
│
├── tests/                      # Tests unitarios
├── .env                        # Variables de entorno (NO subir a Git)
├── requirements.txt            # Dependencias Python
├── run_app.py                  # Punto de entrada principal
└── README.md                   # Este archivo
```

---

## 🔄 Control de Versiones (Git)

### Primer Commit y Push

Si es la primera vez que subes el proyecto:

```bash
# 1. Inicializar repositorio (si no está inicializado)
git init

# 2. Agregar remote (reemplaza con tu URL)
git remote add origin https://github.com/tu-usuario/ProyectoFIS.git

# 3. Agregar archivos al staging
git add .

# 4. Hacer commit
git commit -m "Initial commit: Sistema de Gestión Académica FIS"

# 5. Crear rama principal y hacer push
git branch -M main
git push -u origin main
```

### Commits Posteriores

Para guardar cambios después de trabajar:

```bash
# 1. Ver qué archivos cambiaron
git status

# 2. Agregar archivos específicos o todos
git add archivo.py              # Un archivo específico
git add .                       # Todos los cambios

# 3. Hacer commit con mensaje descriptivo
git commit -m "Descripción clara de los cambios"

# 4. Subir cambios al repositorio remoto
git push
```

### Ejemplos de Mensajes de Commit

```bash
git commit -m "feat: Agregar módulo de calificaciones"
git commit -m "fix: Corregir error en login de usuarios"
git commit -m "docs: Actualizar README con instrucciones"
git commit -m "refactor: Simplificar lógica de permisos"
git commit -m "style: Mejorar diseño del dashboard admin"
```

### Archivo .gitignore

El proyecto incluye un `.gitignore` que excluye:

- `venvFIS/` - Entorno virtual
- `__pycache__/` - Cache de Python
- `.env` - Variables de entorno (sensibles)
- `*.pyc` - Archivos compilados
- `reportes/` - Reportes generados
- `logs/` - Logs con credenciales

**IMPORTANTE:** Nunca subas el archivo `.env` ni el directorio `logs/` con credenciales reales.

---

## 👤 Gestión de Usuarios (CU-03)

### Crear Usuarios desde el Dashboard

El sistema implementa el caso de uso **CU-03: Crear Usuario** con validaciones completas:

1. **Acceso:** Como administrador, ve al dashboard y haz clic en **"➕ Nuevo Usuario"**
2. **Formulario:** Completa todos los campos obligatorios:
   - Username (correo electrónico)
   - Rol (director, profesor, acudiente)
   - Datos personales (nombres, apellidos, identificación)
   - Campos específicos según el rol seleccionado
3. **Contraseña:** Se genera **automáticamente** (12 caracteres seguros)
4. **Guardado:** Las credenciales se guardan en:
   - Base de datos (contraseña encriptada con bcrypt)
   - Archivo `logs/credenciales_usuarios.txt` (contraseña en texto plano para recuperación)
5. **Resultado:** Mensaje de éxito con la contraseña generada

### Recuperar Contraseñas Generadas

Si necesitas recuperar una contraseña generada, consulta el archivo:

```
logs/credenciales_usuarios.txt
```

Este archivo contiene:
- Fecha y hora de creación
- Nombre completo del usuario
- Rol asignado
- Email (username)
- **Contraseña generada** (en texto plano)
- ID del administrador que creó el usuario

**⚠️ Seguridad:** Mantén este archivo seguro. NO lo compartas ni lo subas a repositorios públicos.

### Documentación Detallada

Para más información sobre el flujo completo de creación de usuarios, consulta:

📄 **[docs/CU-03_Crear_Usuario.md](docs/CU-03_Crear_Usuario.md)**

---

## 🏗️ Arquitectura

### Patrón de Arquitectura

El proyecto utiliza **Arquitectura en Capas** con:

- **Capa de Presentación:** Tkinter (app/ui/)
- **Capa de Servicios:** Lógica de negocio (app/services/)
- **Capa de Dominio:** Modelos de entidades (app/core/)
- **Capa de Datos:** Repositorios y ORM (app/data/)

### Patrones de Diseño Implementados

- **Repository Pattern:** Acceso a datos abstraído
- **Unit of Work:** Gestión de transacciones
- **Dependency Injection:** Inyección de dependencias
- **Service Layer:** Lógica de negocio centralizada
- **RBAC:** Control de acceso basado en roles

### Herencia en Modelos

**Administrador:**
- Herencia: `Administrador` → `Usuario` (Joined Table Inheritance)
- Tabla: `administrador.id_administrador` FK a `usuario.id_usuario`

**Otros Roles (Profesor, Directivo, Acudiente):**
- Herencia: Rol → `Persona` (Single Table Inheritance)
- Asociación: FK `id_usuario` en tabla de rol → `usuario.id_usuario`

**Estudiante:**
- Herencia: `Estudiante` → `Persona`
- NO tiene asociación con Usuario

---

## 🛠️ Comandos Útiles

### Desarrollo

```powershell
# Ejecutar la aplicación
python run_app.py

# Ejecutar tests (cuando existan)
python run_tests.py

# Reiniciar completamente la BD
python scripts/reiniciar_bd_completa.py
```

### Base de Datos

```powershell
# Verificar conexión a PostgreSQL
psql -U fis_user -d fis_db_desarrollo -h localhost

# Ver tablas en psql
\dt

# Ver usuarios en psql
SELECT * FROM usuario;

# Ver permisos de un rol
SELECT p.nombre 
FROM permiso p 
JOIN rol_permiso rp ON p.id_permiso = rp.id_permiso 
WHERE rp.id_rol = 1;
```

---

## 📝 Notas Importantes

1. **Siempre activa el entorno virtual** antes de ejecutar scripts Python
2. **Ejecuta `clean_database.sql` ANTES** de los scripts Python
3. **No subas el archivo `.env`** con credenciales reales a Git
4. **Las contraseñas** en la BD están hasheadas con bcrypt
5. **Los permisos** se cargan dinámicamente desde la tabla `permiso`

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'feat: Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de uso académico para la Fundación Internacional de Salud (FIS).

---

## 👨‍💻 Desarrolladores

- **Equipo de Desarrollo FIS**
- **Año:** 2025

---

## 📞 Soporte

Para problemas o dudas sobre el proyecto, consulta la documentación en `docs/` o contacta al equipo de desarrollo.

---

**¡Proyecto configurado y listo para usar!** 🚀
