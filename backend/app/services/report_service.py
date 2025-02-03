from sqlalchemy.orm import Session
from app.services.report_database import get_hired_employees_by_quarter, get_departments_hiring_above_mean

def get_hired_report(db: Session):
    return get_hired_employees_by_quarter(db)

def get_departments_above_mean_report(db: Session):
    return get_departments_hiring_above_mean(db)