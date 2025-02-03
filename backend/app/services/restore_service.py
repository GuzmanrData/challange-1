from pyspark.sql import SparkSession
from sqlalchemy.orm import Session
import os
from sqlalchemy import text
from app.core.config import POSTGRES_URL, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DRIVER, BACKUP_PATH
from app.services.database_service import load_data_to_postgres
from fastapi import HTTPException

def restore_table(db: Session, table_name: str, backup_timestamp: str):
    """
    Restaura una tabla desde un backup en formato AVRO.
    1. Elimina la tabla si existe.
    2. Recrea la tabla con la estructura original.
    3. Inserta los datos desde el backup en AVRO.
    4. Si hay error, hace rollback.
    """
    try:
        print(f"🔄 Restaurando {table_name} desde el backup con timestamp {backup_timestamp}")

        # 📌 Path del backup basado en timestamp
        backup_path = os.path.join(BACKUP_PATH, table_name, f"backup_timestamp={backup_timestamp}")


        # Iniciar sesión de Spark
        spark = SparkSession.builder \
            .appName(f"restore_{table_name}") \
            .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.4.1") \
            .master("local[*]") \
            .getOrCreate()
        
        
        # Verificar si el backup existe
        if not os.path.exists(backup_path):
            raise HTTPException(status_code=404, detail=f"Backup {backup_timestamp} para la tabla {table_name} no encontrado.")
            
        # Leer el backup en formato AVRO
        df = spark.read.format("avro").load(backup_path)
         
                # Eliminar columna de timestamp si existe
        if "backup_timestamp" in df.columns:
            df = df.drop("backup_timestamp")
        
         # 📌 Iniciar transacción en PostgreSQL
        
        db.begin()
            # 📌 Eliminar la tabla antes de restaurarla
        db.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
        
        
             # 📌 Volver a crear la tabla con la estructura original
        create_table_sql = get_create_table_sql(table_name)
        if not create_table_sql:
            raise HTTPException(status_code=400, detail=f"No se encontró la estructura de la tabla {table_name}")
        
        
        #db.execute(text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'active';"))

        db.execute(text(create_table_sql))
        
        db.commit()
        
        df\
            .write \
            .mode("append") \
            .format("jdbc") \
            .option("url", POSTGRES_URL) \
            .option("dbtable", table_name) \
            .option("user", POSTGRES_USER) \
            .option("password", POSTGRES_PASSWORD) \
            .option("driver", POSTGRES_DRIVER) \
            .save()
        #load_data_to_postgres(df, table_name)
        #db.execute(text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'active';"))
        # 📌 Confirmar la transacción si todo salió bien
    

        print(f"✅ Restauración de {table_name} completada exitosamente desde {backup_path}")
        return {"message": f"Restauración de {table_name} desde {backup_timestamp} completada exitosamente."}

    except Exception as e:
        db.rollback()  # Revertir cambios en caso de error
        print(f"❌ Error al restaurar {table_name}")
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        spark.stop()
        print("🛑 Spark session cerrada.")


def get_create_table_sql(table_name: str):
    """
    Devuelve la sentencia SQL para recrear la estructura de una tabla.
    """
    tables_sql = {
        "departments": """
            CREATE TABLE departments (
                id SERIAL PRIMARY KEY,
                department VARCHAR(255) NOT NULL
            );
        """,
        "jobs": """
            CREATE TABLE jobs (
                id SERIAL PRIMARY KEY,
                job VARCHAR(255) NOT NULL
            );
        """,
        "hired_employees": """
            CREATE TABLE hired_employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                datetime TIMESTAMP NOT NULL,
                department_id INT REFERENCES departments(id),
                job_id INT REFERENCES jobs(id)
            );
        """
    }
    return tables_sql.get(table_name)
