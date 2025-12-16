from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ---------- Model ----------
class Student(BaseModel):
    id: int
    name: str
    course: str

# ---------- Fake Database ----------
students = []

# ---------- Routes ----------
@app.get("/")
def root():
    return {"message": "Day 2: Student API"}

@app.get("/students")
def get_students():
    return students

@app.post("/students")
def create_student(student: Student):
    students.append(student)
    return {"message": "Student added successfully", "student": student}
