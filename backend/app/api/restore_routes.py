from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.restore_service import restore_table
from app.core.database import get_db
from pydantic import BaseModel

router = APIRouter()
class RestoreRequest(BaseModel):
    table_name: str
    backup_timestamp: str

@router.post("/restore/")
async def restore_table_api(request: RestoreRequest, db: Session = Depends(get_db)):
    """
    Endpoint para restaurar una tabla desde un backup en AVRO.
    Recibe el nombre de la tabla y el timestamp del backup.
    """
    print(f"🔄 Restaurando {request.table_name} desde el backup con timestamp {request.backup_timestamp}")
    return restore_table(db, request.table_name, request.backup_timestamp)
