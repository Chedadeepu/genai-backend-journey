from fastapi import APIRouter, HTTPException
from models.student import Student

router = APIRouter()

students = []

@router.get("/students")
def get_students():
    return students

@router.post("/students")
def create_student(student: Student):
    for s in students:
        if s.id == student.id:
            raise HTTPException(status_code=400, detail="Student with this ID already exists")
    students.append(student)
    return {"message": "Student added successfully", "student": student}

@router.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for index, s in enumerate(students):
        if s.id == student_id:
            students[index] = updated_student
            return {"message": "Student updated successfully", "student": updated_student}
    raise HTTPException(status_code=404, detail="Student not found")

@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, s in enumerate(students):
        if s.id == student_id:
            deleted = students.pop(index)
            return {"message": "Student deleted successfully", "student": deleted}
    raise HTTPException(status_code=404, detail="Student not found")
