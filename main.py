from fastapi import FastAPI
from database.db import engine
from database import models
from routes.students import router as student_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Day 5: Database Integrated"}

app.include_router(student_router)
