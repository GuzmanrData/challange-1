from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from app.core.config import POSTGRES_URL, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DRIVER
import traceback
from fastapi import HTTPException

def load_data_to_postgres(df, table_name: str):
    """Carga un DataFrame de PySpark a PostgreSQL."""
    try:
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
        print(f"✅ {table_name} guardado correctamente en PostgreSQL.")
    except Exception as e:
        print(f"❌ Error al cargar {table_name} en PostgreSQL: {str(e)}")
        print(traceback.format_exc())
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(status_code=400, detail=f"❌ {table_name} ya ha sido cargado")
            
       
        raise HTTPException(status_code=500, detail=f"❌ Error al cargar {table_name} en PostgreSQL: {str(e)}")
