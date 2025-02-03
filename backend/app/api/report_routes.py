from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.report_service import get_hired_report, get_departments_above_mean_report

router = APIRouter()

@router.get("/hired-employees-report/")
def hired_employees_report(db: Session = Depends(get_db)):
    return get_hired_report(db)

@router.get("/departments-above-mean/")
def departments_above_mean_report(db: Session = Depends(get_db)):
    return get_departments_above_mean_report(db)
