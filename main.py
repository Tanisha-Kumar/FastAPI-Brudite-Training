from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name:str
    age:int
    course:str
    
@app.get("/")
def hello_folks():
    return("message hello folks")

@app.post("/student")
def create_student(data: Student):
    return{
        "message": "Student created successfullly",
        "student": data
    }