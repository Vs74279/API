from fastapi import FastAPI,Depends,HTTPException,status
from datetime import datetime, timedelta
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext


app= FastAPI()


models.Base.metadata.create_all(bind=engine)


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# T

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@app.post('/student',tags=['Student'])
def create(request: schemas.Student,db: Session =Depends(get_db) ):
    student=models.Student(name=request.name,age=request.age)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@app.get('/student',tags=['Student'])
def all_student(db: Session =Depends(get_db)):
    student=db.query(models.Student).all()
    return student

@app.get('/student/{id}',tags=['Student'])
def all_student(id,db: Session =Depends(get_db)):
    student=db.query(models.Student).filter(models.Student.id==id).first()
    return student

@app.delete('/student/{id}',tags=['Student'])
def delete(id,db :Session =Depends(get_db)):
    student=db.query(models.Student).filter(models.Student.id==id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='student are not available')
    db.delete(student)
    db.commit()
    return student

@app.put('/student/{id}',tags=['Student'])
def update(id,request : schemas.Student,db :Session =Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id==id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='student are not available')
    student.name=request.name
    student.age=request.age
    db.commit()
    db.refresh(student)
    return student

@app.post('/user',tags=['user'])
def register(request:schemas.User,db :Session =Depends(get_db)):
    hashed_password=pwd_context.hash(request.password)
    user=models.User(username=request.username,password=hashed_password,role=request.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
@app.post("/login",tags=['user'])
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
    
   





@app.post('/task',tags=['Task'])
def create(request: schemas.Task,db :Session =Depends(get_db)):
    task=models.Task(title=request.title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
@app.get('/task',tags=['Task'])
def all_task(db :Session =Depends(get_db)):
    task=db.query(models.Task).all()
    return task

@app.get('/task/{id}',tags=['Task'])
def get_task(id,db :Session =Depends(get_db)):
    task=db.query(models.Task).filter(models.Task.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='task are not available')
    return task

@app.delete('/task/{id}',tags=['Task'])
def all_task(id,db :Session =Depends(get_db)):
    task=db.query(models.Task).filter(models.Task.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='task are not available')
    db.delete(task)
    db.commit()
    return task

@app.put('/task/{id}',tags=['Task'])
def update(id,request : schemas.Task,db :Session =Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='task are not available')
    task.title=request.title
    db.commit()
    db.refresh(task)
    return task




