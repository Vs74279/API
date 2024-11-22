from sqlalchemy import Column, Integer, String,Boolean
from .database import Base

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)   

class User(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(Integer)
    role = Column(String)

    