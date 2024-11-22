from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age : int

class Task(BaseModel):
       title : str 

class User(BaseModel):
    username: str
    password: str
    role: str

class Login(BaseModel):
    username: str
    password: str
