from fastapi import APIRouter
from app.services.backup_service import backup_table
import datetime

router = APIRouter()

@router.post("/backup/")
async def backup_tables():
    """
    Realiza un backup de todas las tablas (`departments`, `jobs`, `hired_employees`)
    en formato AVRO, particionado por `backup_timestamp`.
    """
    tables = ["departments", "jobs", "hired_employees"]
    results = {}
                # 📌 Generar un timestamp en formato string para los backups
    backup_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


    for table in tables:
        result = backup_table(table,backup_timestamp)
        results[table] = result

    return {"message": "Backups completados", "results": results}
