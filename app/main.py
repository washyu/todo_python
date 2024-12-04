from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
app.mount("/", StaticFiles(directory="todo-app/build", html=True), name="static")

@app.get("/api")
def read_root():
    return {"message": "Welcome to the ToDo API"}

@app.get("/api/todos", response_model=List[schemas.ToDo])
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.ToDoModel).all()

@app.get("/api/todos/{todo_id}", response_model=schemas.ToDo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.ToDoModel).filter(models.ToDoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo

@app.post("/api/todos", response_model=schemas.ToDo)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    db_todo = models.ToDoModel(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/api/todos/{todo_id}", response_model=schemas.ToDo)
def update_todo(todo_id: int, update_todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    todo = db.query(models.ToDoModel).filter(models.ToDoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="ToDo not found")
    for key, value in update_todo.model_dump().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/api/todos/{todo_id}", response_model=schemas.ToDo)
def delete_todo(todo_id: int,  db: Session = Depends(get_db)):
    todo = db.query(models.ToDoModel).filter(models.ToDoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="ToDo not found")
    db.delete(todo)
    db.commit()
    return todo