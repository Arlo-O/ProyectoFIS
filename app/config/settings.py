"""
settings.py - Variables de entorno y configuración global

Define todas las variables de configuración centralizadas desde .env
y proporciona valores por defecto seguros.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# BASE DE DATOS
# ============================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://fis_user:fis_password@localhost:5432/fis_db_desarrollo"
)
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

# ============================================
# AMBIENTE
# ============================================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_DEVELOPMENT = ENVIRONMENT == "development"
IS_PRODUCTION = ENVIRONMENT == "production"

# ============================================
# CREDENCIALES DE PRUEBA (solo desarrollo)
# ============================================
TEST_ADMIN_EMAIL = os.getenv("TEST_ADMIN_EMAIL", "admin@colegio.edu")
TEST_ADMIN_PASSWORD = os.getenv("TEST_ADMIN_PASSWORD", "admin123")

TEST_DIRECTOR_EMAIL = os.getenv("TEST_DIRECTOR_EMAIL", "director@colegio.edu")
TEST_DIRECTOR_PASSWORD = os.getenv("TEST_DIRECTOR_PASSWORD", "director123")

TEST_TEACHER_EMAIL = os.getenv("TEST_TEACHER_EMAIL", "profesor@colegio.edu")
TEST_TEACHER_PASSWORD = os.getenv("TEST_TEACHER_PASSWORD", "profesor123")

TEST_STUDENT_EMAIL = os.getenv("TEST_STUDENT_EMAIL", "estudiante@colegio.edu")
TEST_STUDENT_PASSWORD = os.getenv("TEST_STUDENT_PASSWORD", "estudiante123")

# ============================================
# RUTAS DE ARCHIVOS
# ============================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(BASE_DIR, "reportes")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Crear directorios si no existen
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
