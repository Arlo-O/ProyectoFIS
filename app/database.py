from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

DATABASE_URL = "postgresql+psycopg2://fis_user:fis_password@localhost:5432/fis_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


def init_db():
    """Crea todas las tablas en la base de datos"""
    # Importar modelos ORM para que se registren
    from modelos import orm_models
    Base.metadata.create_all(bind=engine)


def get_db():
    """Obtiene una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Contexto manager para sesiones de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
