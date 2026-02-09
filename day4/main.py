from resume_extractor import process_resumes
from resume_analyzer import analyzing_pipeline
import json

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Resume Evaluator API")
output_file = "resume_data.json"

@app.post("/evaluate")
def evaluate_resume(request: str):
        # Phase 1: Extract the content of resumes in markdown format
        md_list = process_resumes(request)

        # Phase 2: Analyze the content of resumes using LLM and save the output in json file
        analyzing_pipeline(md_list)