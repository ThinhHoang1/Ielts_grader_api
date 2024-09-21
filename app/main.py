# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .models import EssayInput, CheckResponse, GradeResponse
from .grader import check_essay, grade_essay

app = FastAPI(
    title="IELTS Writing Grader API",
    description="An API to check spelling, grammar, and grade IELTS essays using Google Generative AI.",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the IELTS Writing Grader API!"}

@app.post("/check-spelling", response_model=CheckResponse)
async def api_check_spelling(essay_input: EssayInput):
    try:
        result = check_essay("Check spelling in", essay_input.essay)
        return CheckResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-grammar", response_model=CheckResponse)
async def api_check_grammar(essay_input: EssayInput):
    try:
        result = check_essay("Check grammar in", essay_input.essay)
        return CheckResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grade-essay", response_model=GradeResponse)
async def api_grade_essay(essay_input: EssayInput):
    try:
        grading_result = grade_essay(essay_input.title, essay_input.essay)
        return GradeResponse(
            feedback=grading_result["feedback"],
            grade_band=grading_result["grade_band"],
            word_count=grading_result["word_count"],
            warning=grading_result["warning"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
