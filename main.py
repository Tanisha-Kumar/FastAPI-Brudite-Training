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

USERS = {
    "1a" : {"name": "Alice", "age": 21},
    "2b" : {"name": "Bob", "age": 22},
    "3c" : {"name": "Charlie", "age": 23}
}

@app.get("/user/{user_id}")
def get_user(user_id: str):
    user = USERS.get(user_id)
    if user:
        return{"user_id": user_id, "user": user}
    return{"message": "User not found"}