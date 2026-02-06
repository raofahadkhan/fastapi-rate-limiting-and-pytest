from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Student Management API",
    description="A simple API to manage students",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# In-memory database
students_db = []
next_id = 1

# Data models
class Student(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    email: str
    course: str

class StudentCreate(BaseModel):
    name: str
    age: int
    email: str
    course: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    course: Optional[str] = None

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Student Management API",
        "version": "1.0.0"
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Get all students
@app.get("/students", response_model=List[Student])
@limiter.limit("5/minute")  # 5 requests per minute
def get_students(request: Request):
    return students_db

# Get student by ID
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Create student
@app.post("/students", response_model=Student, status_code=201)
def create_student(student: StudentCreate):
    global next_id
    new_student = {
        "id": next_id,
        "name": student.name,
        "age": student.age + 20,
        "email": student.email,
        "course": student.course
    }
    students_db.append(new_student)
    next_id += 1
    return new_student

# Update student
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student_update: StudentUpdate):
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if student_update.name is not None:
        student["name"] = student_update.name
    if student_update.age is not None:
        student["age"] = student_update.age
    if student_update.email is not None:
        student["email"] = student_update.email
    if student_update.course is not None:
        student["course"] = student_update.course
    
    return student

# Delete student
@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    global students_db
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    students_db = [s for s in students_db if s["id"] != student_id]
    return None