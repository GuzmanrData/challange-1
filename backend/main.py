from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy import text
from pyspark.sql import SparkSession
import os
import json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType
from pyspark.sql.functions import lit, current_timestamp, col, length
import traceback





 # Directorios de entrada y salida
LANDING_PATH = "landing"
SILVER_PATH = "silver"
GOLD_PATH = "gold"

# Crear carpetas si no existen
os.makedirs(LANDING_PATH, exist_ok=True)
os.makedirs(SILVER_PATH, exist_ok=True)
os.makedirs(GOLD_PATH, exist_ok=True)

# Configurar la conexión al cluster de Spark
#SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL", "spark://spark_cluster:7077")



# Directorios de entrada
DEPARTMENTS_PATH = os.path.join(LANDING_PATH, "departments_")
JOBS_PATH = os.path.join(LANDING_PATH, "jobs_")
HIRED_EMPLOYEES_PATH = os.path.join(LANDING_PATH, "hired_employees_")

# Directorios de los schemas
DEPARTMENTS_SCHEMA_PATH = os.path.join("schemas", "department_schema.json")
EMPLOYEES_SCHEMA_PATH = os.path.join("schemas", "employees_schema.json")
JOBS_SCHEMA_PATH = os.path.join("schemas", "jobs_schema.json")

app = FastAPI()


@app.post("/upload-csv/")
async def upload_csv(
    process_date: str,
):
    try:
        print(process_date)
        # Conectar al Spark Master en el otro contenedor
        spark = SparkSession.builder \
            .appName("myapp") \
            .config("spark.jars", "app/jars/postgresql-42.5.0.jar") \
            .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.4.1") \
            .master("local[*]") \
            .getOrCreate()
            
        # Leer el esquema desde el archivo JSON
        with open(DEPARTMENTS_SCHEMA_PATH, "r") as f:
            department_schema = json.load(f)
            
        # Generar el esquema desde el JSON
        department_schema = json_to_struct(department_schema)
                    
                    
                               
        # Leer el esquema desde el archivo JSON
        with open(EMPLOYEES_SCHEMA_PATH, "r") as f:
            employees_schema = json.load(f)
            
        # Generar el esquema desde el JSON
        employees_schema = json_to_struct(employees_schema)
        
        
               # Leer el esquema desde el archivo JSON
        with open(JOBS_SCHEMA_PATH, "r") as f:
            jobs_schema = json.load(f)
            
        # Generar el esquema desde el JSON
        jobs_schema = json_to_struct(jobs_schema)
        
        

        # Leer el CSV con PySpark
        department_df = spark.read.csv(DEPARTMENTS_PATH  + process_date + ".csv", header=False, schema=department_schema) \
        .withColumn("process_date", lit(process_date))\
        .withColumn("load_timestamp", current_timestamp())
        
        employees_df = spark.read.csv(HIRED_EMPLOYEES_PATH + process_date + ".csv", header=False, schema=employees_schema) \
        .withColumn("process_date", lit(process_date))\
        .withColumn("load_timestamp", current_timestamp())
        
        jobs_df = spark.read.csv(JOBS_PATH  + process_date + ".csv", header=False, schema=jobs_schema) \
        .withColumn("process_date", lit(process_date))\
        .withColumn("load_timestamp", current_timestamp())
        

        # Cargar la data en postgreSQL
        errors = []
        
        
#ejecutar esta consulta: TRUNCATE TABLE hired_employees RESTART IDENTITY CASCADE;
         
        
#TRUNCATE TABLE jobs RESTART IDENTITY CASCADE;
#TRUNCATE TABLE departments RESTART IDENTITY CASCADE;
     
        employees_df.show()
        
        employees_df.drop("process_date", "load_timestamp") \
        .filter(col("datetime").isNotNull()) \
        .filter(length(col("name")) < 255) \
        .write \
        .mode("append") \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres_db:5432/coding_challenge") \
        .option("dbtable", "hired_employees") \
        .option("user", "user") \
        .option("password", "password") \
        .option("driver", "org.postgresql.Driver") \
        .save()
        print("✅ Employees guardado correctamente en PostgreSQL.")

   
            
        spark.stop()
                
                
        return {"message": "Data uploaded successfully", "errors": errors}
        
    except Exception as e:
        print("Error en la carga de datos")
        print(e)
        if "duplicate key value violates unique constraint" in str(e):
            return {"message": "Data already uploaded"}
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": str(e)}
    
    
    
    
# Convertir el JSON en un StructType dinámicamente
def json_to_struct(schema_json):
    type_mapping = {
        "integer": IntegerType(),
        "string": StringType(),
        "timestamp": TimestampType(),
        # Agrega más tipos si los necesitas (DoubleType, BooleanType, etc.)
    }
    fields = [
        StructField(field["name"], type_mapping[field["type"]], field["nullable"])
        for field in schema_json["fields"]
    ]
    return StructType(fields)