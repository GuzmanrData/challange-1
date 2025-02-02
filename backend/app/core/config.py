from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType
import json

import os

# Directorios base
LANDING_PATH = "landing"
SILVER_PATH = "silver"
GOLD_PATH = "gold"
SCHEMA_PATH = "schemas"

# Crear carpetas si no existen
for path in [LANDING_PATH, SILVER_PATH, GOLD_PATH, SCHEMA_PATH]:
    os.makedirs(path, exist_ok=True)

# Configuración de la base de datos
POSTGRES_URL = "jdbc:postgresql://postgres_db:5432/coding_challenge"
POSTGRES_USER = "user"
POSTGRES_PASSWORD = "password"
POSTGRES_DRIVER = "org.postgresql.Driver"

def json_to_struct(schema_path: str) -> StructType:
    """Convierte un archivo JSON a StructType de PySpark."""
    type_mapping = {
        "integer": IntegerType(),
        "string": StringType(),
        "timestamp": TimestampType(),
    }

    try:
        with open(schema_path, "r") as f:
            schema_json = json.load(f)

        fields = [
            StructField(field["name"], type_mapping[field["type"]], field["nullable"])
            for field in schema_json["fields"]
        ]
        return StructType(fields)

    except Exception as e:
        raise ValueError(f"Error al cargar el esquema JSON: {str(e)}")
