from fastapi import FastAPI,Depends,HTTPException,status

from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
app= FastAPI()


models.Base.metadata.create_all(bind=engine)

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



