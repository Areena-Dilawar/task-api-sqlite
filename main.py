import sqlite3

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD Task API built with FastAPI and SQLite.",
    version="2.0"
)

# Database Connection

connection = sqlite3.connect("tasks.db", check_same_thread=False)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# Create Table

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
)
""")

connection.commit()


# Seed Data 

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    sample_tasks = [
        ("Learn FastAPI", False),
        ("Build CRUD API", False),
        ("Submit Assignment", False),
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        sample_tasks
    )

    connection.commit()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Submit Assignment", "done": False},
]


@app.get("/", summary="API Information")
def root():
    return {
        "name": "Task API",
        "version": "2.0",
        "database": "SQLite",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Health Check")
def health():
    return {
        "status": "ok"
    }


@app.get("/tasks", summary="Get all tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Get task by ID")
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post(
    "/tasks",
    summary="Create a new task",
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate):

    title = task.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, updated_task: TaskUpdate):

    title = updated_task.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title
            task["done"] = updated_task.done
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete(
    "/tasks/{task_id}",
    summary="Delete a task",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )