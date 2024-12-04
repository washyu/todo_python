import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
import app as models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todos.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos", json={"title": "Test ToDo", "description": "Test Description", "completed": False})
    assert response.status_code == 200
    assert response.json()["title"] == "Test ToDo"
    assert response.json()["description"] == "Test Description"
    assert response.json()["completed"] is False

def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_todo():
    response = client.post("/todos", json={"title": "Test ToDo", "description": "Test Description", "completed": False})
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test ToDo"

def test_update_todo():
    response = client.post("/todos", json={"title": "Test ToDo", "description": "Test Description", "completed": False})
    todo_id = response.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "Updated ToDo", "description": "Updated Description", "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated ToDo"
    assert response.json()["description"] == "Updated Description"
    assert response.json()["completed"] is True

def test_delete_todo():
    response = client.post("/todos", json={"title": "Test ToDo", "description": "Test Description", "completed": False})
    todo_id = response.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test ToDo"
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404