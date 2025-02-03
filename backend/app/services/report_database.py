from sqlalchemy.orm import Session
from sqlalchemy import text

def get_hired_employees_by_quarter(db: Session):
    query = text("""
        SELECT 
            d.department, 
            j.job,
            SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        JOIN jobs j ON he.job_id = j.id
        WHERE EXTRACT(YEAR FROM he.datetime) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department ASC, j.job ASC
    """)

    result = db.execute(query)
    return [dict(row._mapping) for row in result]

def get_departments_hiring_above_mean(db: Session):
    query = text("""
        WITH department_hiring AS (
            SELECT 
                d.id,
                d.department,
                COUNT(he.id) AS hired
            FROM hired_employees he
            JOIN departments d ON he.department_id = d.id
            WHERE EXTRACT(YEAR FROM he.datetime) = 2021
            GROUP BY d.id, d.department
        ), 
        overall_mean AS (
            SELECT AVG(hired) AS mean_hired FROM department_hiring
        )
        SELECT dh.id, dh.department, dh.hired
        FROM department_hiring dh
        JOIN overall_mean om ON dh.hired > om.mean_hired
        ORDER BY dh.hired DESC;
    """)

    result = db.execute(query)
    return [dict(row._mapping) for row in result]
