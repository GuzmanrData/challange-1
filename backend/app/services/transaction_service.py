from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from app.utils.validation import BatchInsertRequest

def insert_batch_data(db: Session, request: BatchInsertRequest):
    """
    Inserta múltiples registros en PostgreSQL dentro de una transacción.
    Si el departamento, trabajo o empleado ya existe, no lo inserta.
    Los IDs de departamentos, trabajos y empleados son enviados en el body.
    """
    BATCH_SIZE_LIMIT = 1000

    # Validar el tamaño del batch
    total_records = len(request.departments) + len(request.jobs) + len(request.hired_employees)
    if total_records > BATCH_SIZE_LIMIT:
        raise HTTPException(status_code=400, detail=f"Batch size exceeds limit of {BATCH_SIZE_LIMIT} rows (Received: {total_records})")
    
    try:
    
        db.begin()  # Iniciar la transacción manualmente
        if request.departments:
                db.execute(text("SELECT setval('departments_id_seq', COALESCE((SELECT MAX(id) FROM departments), 1), false);"))
                db.execute(text("SELECT nextval('departments_id_seq');"))   
                for department in request.departments:
                    
                    existing_department = db.execute(
                        text("SELECT id FROM departments WHERE department = :department"),
                        {"department": department.department}
                    ).fetchone()

                    if not existing_department:
                        db.execute(
                            text("INSERT INTO departments (department) VALUES (:department)"),
                            {"department": department.department}
                        )
                    

        # Insertar trabajos evitando duplicados (buscando por nombre)
        if request.jobs:
            db.execute(text("SELECT setval('jobs_id_seq', COALESCE((SELECT MAX(id) FROM jobs), 1), false);"))
            db.execute(text("SELECT nextval('jobs_id_seq');"))
                
            for job in request.jobs:
                    
                existing_job = db.execute(
                    text("SELECT id FROM jobs WHERE job = :job"),
                    {"job": job.job}
                ).fetchone()

                if not existing_job:
                        
                    db.execute(
                        text("INSERT INTO jobs (job) VALUES (:job)"),
                        {"job": job.job}
                    )
                    


        # Insertar empleados contratados evitando duplicados por ID
        if request.hired_employees:
            db.execute(text("SELECT setval('hired_employees_id_seq', COALESCE((SELECT MAX(id) FROM hired_employees), 1), false);"))
            db.execute(text("SELECT nextval('hired_employees_id_seq');"))
            for employee in request.hired_employees:
                    db.execute(text("""
                        INSERT INTO hired_employees (name, datetime, department_id, job_id) 
                        VALUES (:name, :datetime, :department_id, :job_id)
                    """), {
                        "name": employee.name,
                        "datetime": employee.datetime,
                        "department_id": employee.department_id,
                        "job_id": employee.job_id
                    })
                    
                    #d
        
        
        db.commit()  # Confirmar la transacción si no hubo errores

        return {"message": "Batch insert completed successfully"}

    except Exception as e:
        db.rollback()  # Revertir la transacción si hubo un error
        
        print("❌ Error during batch insert")
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

