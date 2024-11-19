from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age : int

class Task(BaseModel):
       title : str 