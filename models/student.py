from pydantic import BaseModel

class StudentCreate(BaseModel):
    id: int
    name: str
    course: str

class StudentResponse(BaseModel):
    id: int
    name: str
    course: str

    class Config:
        from_attributes = True
