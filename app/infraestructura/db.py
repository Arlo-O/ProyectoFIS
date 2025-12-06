import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

# Define the database URL.
# Using PostgreSQL with provided credentials.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:juanesgc1@localhost:5432/gestionacademica")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

# Create the registry for imperative mapping
mapper_registry = registry()
