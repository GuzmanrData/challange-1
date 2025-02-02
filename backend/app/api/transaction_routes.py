from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.validation import BatchInsertRequest
from app.services.transaction_service import insert_batch_data
from app.core.database import get_db

router = APIRouter()

@router.post("/insert-batch/")
async def insert_batch(request: BatchInsertRequest, db: Session = Depends(get_db)):
    """
    Inserta múltiples registros en PostgreSQL en una sola solicitud.

    Body:
    {
        "departments": [...],
        "jobs": [...],
        "hired_employees": [...]
    }
    """
    return insert_batch_data(db, request)
