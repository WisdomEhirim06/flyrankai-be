from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="To-Do API")

# The Schema
class TaskCreate(BaseModel):
    task: str
    done: bool = False

# Schema for outgoing task data (includes ID)
class Task(TaskCreate):
    id: int


tasks: List[Task] = []
id_counter = 1

@app.get("/")
def home():
    return {"message": "Your To-Do list is on"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    global id_counter
    new_task = Task(id=id_counter, **task_data.model_dump())
    tasks.append(new_task)
    id_counter += 1
    return new_task

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, message="Task not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, message="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskCreate):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = Task(id=task_id, **task_data.model_dump())
            tasks[idx] = updated_task
            return updated_task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")