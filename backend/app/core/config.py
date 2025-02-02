from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType
import json

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
