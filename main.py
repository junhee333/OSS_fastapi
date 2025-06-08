from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conint
from typing import List, Literal

gpa_service = FastAPI()

GRADE_TO_POINT = {
    "A+": 4.5,
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "F": 0.0,
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: conint(ge=1)
    grade: Literal["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]

class StudentRequest(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

class StudentSummary(BaseModel):
    student_id: str
    name: str
    gpa: float
    total_credits: int

class GradeResponse(BaseModel):
    student_summary: StudentSummary


@gpa_service.post("/score", response_model=GradeResponse)
async def grade_student(student: StudentRequest):
    total_points = 0.0
    total_credits = 0

    if not student.courses:
        raise HTTPException(status_code=400, detail="courses 목록이 비어 있습니다.")

    for course in student.courses:
        point = GRADE_TO_POINT[course.grade]
        total_points += point * course.credits
        total_credits += course.credits
    gpa = total_points / total_credits
    gpa = round(gpa + 1e-8, 2)

    summary = StudentSummary(
        student_id=student.student_id,
        name=student.name,
        gpa=gpa,
        total_credits=total_credits
    )

    return GradeResponse(student_summary=summary)