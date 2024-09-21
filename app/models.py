# app/models.py
from pydantic import BaseModel, Field
from typing import Optional

class EssayInput(BaseModel):
    title: str = Field(..., example="The Impact of Technology on Education")
    essay: str = Field(..., example="Your IELTS essay content goes here.")

class CheckResponse(BaseModel):
    result: str

class GradeResponse(BaseModel):
    feedback: str
    grade_band: Optional[float] = None
    word_count: int
    warning: Optional[str] = None
