from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Department(BaseModel):
    id: Optional[int] = None  # Hacemos el ID opcional
    department: str = Field(..., min_length=2, max_length=255)

class Job(BaseModel):
    id: Optional[int] = None  # Hacemos el ID opcional
    job: str = Field(..., min_length=2, max_length=255)

class HiredEmployee(BaseModel):
    id: Optional[int] = None  # Hacemos el ID opcional
    name: str = Field(..., min_length=2, max_length=255)
    datetime: datetime
    department_id: int = Field(..., gt=0)
    job_id: int = Field(..., gt=0)

class BatchInsertRequest(BaseModel):
    departments: List[Department] = []
    jobs: List[Job] = []
    hired_employees: List[HiredEmployee] = []
