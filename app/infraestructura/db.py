import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

# Configuración de la base de datos PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:juanesgc1@localhost:5432/gestionacademica")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
mapper_registry = registry()