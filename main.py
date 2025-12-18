from fastapi import FastAPI
from routes.students import router as student_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Day 4: Clean Backend Structure"}

app.include_router(student_router)
