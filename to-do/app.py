import sqlite3
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="To-Do API")

# Added to allow the html file to connect to my backend api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "tasks.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        conn.commit()

init_db()

# The Schema
class TaskCreate(BaseModel):
    task: str
    done: bool = False

# Schema for outgoing task data (includes ID)
class Task(TaskCreate):
    id: int


@app.get("/")
def home():
    return {"message": "Your To-Do list is on"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (task, done) VALUES (?, ?)",
            (task_data.task, task_data.done)
        )
        conn.commit()
        task_id = cursor.lastrowid
        cursor.execute("SELECT id, task, done FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return Task(id=row["id"], task=row["task"], done=bool(row["done"]))

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, done FROM tasks")
        rows = cursor.fetchall()
        return [Task(id=row["id"], task=row["task"], done=bool(row["done"])) for row in rows]

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, done FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return Task(id=row["id"], task=row["task"], done=bool(row["done"]))

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET task = ?, done = ? WHERE id = ?",
            (task_data.task, task_data.done, task_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        cursor.execute("SELECT id, task, done FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return Task(id=row["id"], task=row["task"], done=bool(row["done"]))