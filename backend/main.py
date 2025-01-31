from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy import text


app = FastAPI()

@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": str(e)}