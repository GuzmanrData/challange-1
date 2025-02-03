from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp
from app.utils.json_schema import json_to_struct
import traceback
from fastapi import HTTPException

def process_and_save_avro(input_path: str, output_path: str, schema_path: str, process_date: str):
    """Carga un CSV en PySpark, aplica esquema y guarda en formato Avro."""
    try:
        # Iniciar sesión de Spark
        spark = SparkSession.builder \
            .appName("save_avro") \
            .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.4.1") \
            .master("local[*]") \
            .getOrCreate()

        # Cargar esquema JSON
        schema = json_to_struct(schema_path)

        # Leer CSV con PySpark
        df = spark.read.csv(input_path, header=False, schema=schema) \
            .withColumn("process_date", lit(process_date)) \
            .withColumn("load_timestamp", current_timestamp())

        # Guardar como Avro
        df.write.partitionBy("process_date") .mode("overwrite").format("avro").save(output_path)
        print(f"✅ Archivo guardado en {output_path}")

        return output_path

    except Exception as e:
        print("Error en el proceso de conversión a Avro")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if spark:
            spark.stop()
            print("🛑 Spark session cerrada.")
