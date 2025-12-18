from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    course: str
