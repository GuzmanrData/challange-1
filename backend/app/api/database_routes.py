from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.database_service import load_data_to_postgres
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp
from app.utils.json_schema import json_to_struct
import traceback
from pyspark.sql.functions import lit, current_timestamp, col, length
import os
import httpx
from typing import List


router = APIRouter()
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

class LoadDataRequest(BaseModel):
    input_path: str
    schema_path: str
    table_name: str
    process_date: str

@router.post("/load_historical_data/")
async def load_data(request: LoadDataRequest):
    """
    Carga datos desde un archivo CSV a PostgreSQL.

    Body:
    {
        "input_path": "ruta/del/csv.csv",
        "schema_path": "ruta/del/schema.json",
        "table_name": "nombre_de_tabla",
        "process_date": "YYYY-MM-DD"
    }
    """
    try:
        print(f"🔄 Cargando datos en la tabla {request.table_name} desde {request.input_path}")

        # Iniciar sesión de Spark
        spark = SparkSession.builder \
            .appName(f"load_{request.table_name}") \
            .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.4.1") \
            .master("local[*]") \
            .getOrCreate()

        # Cargar el esquema JSON
        schema = json_to_struct(request.schema_path)

        # Leer el CSV con PySpark
        df = spark.read.csv(request.input_path, header=False, schema=schema) \
            
        cleanDf = cleanDataFrmae(df, request.table_name)
      

        # Guardar en PostgreSQL
        load_data_to_postgres(cleanDf, request.table_name)


        return {"message": f"{request.table_name} loaded successfully"}

    except Exception as e:
        print(f"❌ Error al cargar {request.table_name}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if spark:
            spark.stop()
            print("🛑 Spark session cerrada.")

@router.post("/batch-load-historical-data/")
async def batch_load_historical_data(data: List[LoadDataRequest]):
    """
    Carga múltiples archivos CSV en PostgreSQL llamando al endpoint '/load_historical_data/'.

    Body:
    [
        {
            "input_path": "ruta/del/csv.csv",
            "schema_path": "ruta/del/schema.json",
            "table_name": "nombre_de_tabla",
            "process_date": "YYYY-MM-DD"
        },
        {
            "input_path": "ruta/del/otro.csv",
            "schema_path": "ruta/del/otro_schema.json",
            "table_name": "otra_tabla",
            "process_date": "YYYY-MM-DD"
        }
    ]
    """
    results = []

    async with httpx.AsyncClient() as client:
        for entry in data:
            try:
                response = await client.post(f"{FASTAPI_URL}/load_historical_data/", json=entry.dict())
                response_data = response.json()

                if response.status_code == 200:
                    results.append({"status": "success", "file": entry.input_path})
                else:
                    results.append({"status": "error", "message": response_data.get("detail"), "data": entry})

            except Exception as e:
                results.append({"status": "error", "message": str(e), "data": entry})

    return {"message": "Batch processing completed", "results": results}

def cleanDataFrmae(df, table_name):
    
    if(table_name == "departments"):
        return df.filter(col("department").isNotNull())
    
    elif(table_name == "hired_employees"):
        return df.filter(col("datetime").isNotNull())\
                .filter(length(col("name")) < 255)
                
    elif(table_name == "jobs"):
        return df.filter(col("job").isNotNull())
            
