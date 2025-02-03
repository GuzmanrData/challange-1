from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy import text
import os
import json
import traceback
from app.api import avro_routes, database_routes, transaction_routes, backup_routes, restore_routes, report_routes

app = FastAPI()

# Incluir las rutas del API
app.include_router(restore_routes.router)

app.include_router(avro_routes.router)
app.include_router(database_routes.router)
app.include_router(transaction_routes.router)
app.include_router(backup_routes.router)
app.include_router(report_routes.router)



@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": str(e)}
    