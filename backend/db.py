from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Leer la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/coding_challenge")

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear una sesión para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
