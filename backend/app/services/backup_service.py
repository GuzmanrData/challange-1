from pyspark.sql import SparkSession
import os
from app.core.config import POSTGRES_URL, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DRIVER, BACKUP_PATH

def backup_table(table_name: str, backup_timestamp: str):
    """
    Lee una tabla desde PostgreSQL con Apache Spark y la guarda en formato AVRO,
    particionada por la fecha del backup.
    """
    try:

        # Iniciar sesión de Spark
        spark = SparkSession.builder \
            .appName(f"backup_{table_name}") \
            .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.4.1") \
            .master("local[*]") \
            .getOrCreate()

        # Leer la tabla desde PostgreSQL
        df = spark.read \
            .format("jdbc") \
            .option("url", POSTGRES_URL) \
            .option("dbtable", table_name) \
            .option("user", POSTGRES_USER) \
            .option("password", POSTGRES_PASSWORD) \
            .option("driver", POSTGRES_DRIVER) \
            .load()
        
           # 📌 Concatenar el timestamp en la ruta de salida
        table_backup_path = os.path.join(BACKUP_PATH, f"{table_name}/backup_timestamp={backup_timestamp}")


        # Guardar en formato AVRO particionado por `backup_timestamp`
        df.write \
            .mode("overwrite") \
            .format("avro") \
            .save(table_backup_path)

        print(f"✅ Backup de {table_name} completado en {table_backup_path}")
        return {"message": f"Backup de {table_name} completado."}

    except Exception as e:
        print(f"❌ Error en el backup de {table_name}")
        print(e)
        return {"error": str(e)}
    finally:
        if spark:
            spark.stop()
            print("🛑 Spark session cerrada.")