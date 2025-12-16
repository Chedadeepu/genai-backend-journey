from fastapi import FastAPI, HTTPException
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
    return {"message": "Day 3: Complete CRUD API"}

@app.get("/students")
def get_students():
    return students

@app.post("/students")
def create_student(student: Student):
    # Prevent duplicate ID
    for s in students:
        if s.id == student.id:
            raise HTTPException(status_code=400, detail="Student with this ID already exists")
    students.append(student)
    return {"message": "Student added successfully", "student": student}

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for index, s in enumerate(students):
        if s.id == student_id:
            students[index] = updated_student
            return {"message": "Student updated successfully", "student": updated_student}
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, s in enumerate(students):
        if s.id == student_id:
            deleted = students.pop(index)
            return {"message": "Student deleted successfully", "student": deleted}
    raise HTTPException(status_code=404, detail="Student not found")
