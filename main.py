from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends
from db.deps import get_db
from models.student import Student

app = FastAPI()

class StudentReq(BaseModel):
    name:str
    age:int
    course:str
    
#get method
@app.get("/")
def hello_folks():
    return("message hello folks")

#post method
@app.post("/student")
def create_student(data: StudentReq):
    return{
        "message": "Student created successfullly",
        "student": data
    }

USERS = {
    "1a" : {"name": "Alice", "age": 21},
    "2b" : {"name": "Bob", "age": 22},
    "3c" : {"name": "Charlie", "age": 23}
}


#path parameter 
@app.get("/user/{user_id}")
def get_user(user_id: str):
    user = USERS.get(user_id)
    if user:
        return{"user_id": user_id, "user": user}
    return{"message": "User not found"}

#query parameter
@app.get("/user")
def get_all_users(user_id: str = None):
    if user_id:
        user = USERS.get(user_id)
        if user:
            return{"user_id": user_id, "user": user}
        return{"message": "User not found"}
    return{"users": USERS}


@app.post("/students")
def create_student_db(data: StudentReq, db = Depends(get_db)):
    new_student = Student(
        name = data.name,
        age = data.age,
        course = data.course
    )

    db.add(new_student)

    db.commit()
    db.referesh(new_student)

    return new_student