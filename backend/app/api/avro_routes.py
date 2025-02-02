from fastapi import APIRouter, HTTPException
from app.services.avro_service import process_and_save_avro
import os
from typing import List
import httpx

router = APIRouter()

# URL del servicio FastAPI local (ajústala si es necesario)
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

@router.post("/save-avro/")
async def save_avro(data: dict):
    """
    Recibe la información de la tabla a ingestar y guarda el archivo en Avro.

    Body:
    {
        "input_path": "ruta del CSV",
        "output_path": "ruta de salida",
        "schema_path": "ruta del esquema JSON",
        "process_date": "YYYY-MM-DD"
    }
    """
    try:
        input_path = data.get("input_path")
        output_path = data.get("output_path")
        schema_path = data.get("schema_path")
        process_date = data.get("process_date")

        if not all([input_path, output_path, schema_path, process_date]):
            raise HTTPException(status_code=400, detail="Todos los campos son obligatorios")

        saved_path = process_and_save_avro(input_path, output_path, schema_path, process_date)
        return {"message": "Avro file saved successfully", "file": saved_path}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/load-all-data/")
async def load_all_data(data: List[dict]):
    """
    Carga múltiples archivos llamando al endpoint '/save-avro/' de forma asíncrona.

    Body:
    [
        {
            "input_path": "landing/departments_2024-12-31.csv",
            "output_path": "silver/departments",
            "schema_path": "schemas/department_schema.json",
            "process_date": "2024-12-31"
        },
        {
            "input_path": "landing/jobs_2024-12-31.csv",
            "output_path": "silver/jobs",
            "schema_path": "schemas/jobs_schema.json",
            "process_date": "2024-12-31"
        }
    ]
    """
    results = []

    async with httpx.AsyncClient() as client:
        for entry in data:
            try:
                print(f"Processing entry: {entry}")

                response = await client.post(f"{FASTAPI_URL}/save-avro/", json=entry)
                response_data = response.json()

                if response.status_code == 200:
                    results.append({"status": "success", "file": response_data.get("file")})
                else:
                    results.append({"status": "error", "message": response_data.get("detail"), "data": entry})

            except Exception as e:
                results.append({"status": "error", "message": str(e), "data": entry})

    return {"message": "All data processing completed", "results": results}
