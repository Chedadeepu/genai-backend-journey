from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import Student as StudentModel
from models.student import Student

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()

@router.post("/students")
def create_student(student: Student, db: Session = Depends(get_db)):
    existing = db.query(StudentModel).filter(StudentModel.id == student.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student with this ID already exists")

    db_student = StudentModel(
        id=student.id,
        name=student.name,
        course=student.course
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.put("/students/{student_id}")
def update_student(student_id: int, student: Student, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.name = student.name
    db_student.course = student.course
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}
