import sqlite3

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel


app = FastAPI(
    title="Task API",
    description="A simple CRUD Task API built with FastAPI and SQLite.",
    version="2.0"
)


DATABASE = "tasks.db"


# Database Connection Function

def get_connection():
    conn = sqlite3.connect(
        DATABASE,
        check_same_thread=False,
        timeout=10
    )

    conn.row_factory = sqlite3.Row

    return conn



conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
)
""")

conn.commit()


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

    conn.commit()


conn.close()



# Pydantic Models

class TaskCreate(BaseModel):
    title: str



class TaskUpdate(BaseModel):
    title: str
    done: bool




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



# GET ALL TASKS

@app.get("/tasks", summary="Get all tasks")
def get_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]



# GET SINGLE TASK

@app.get("/tasks/{task_id}", summary="Get task by ID")
def get_task(task_id: int):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    conn.close()


    if row is None:

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )


    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }



# CREATE TASK

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


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, False)
    )


    conn.commit()


    new_id = cursor.lastrowid


    conn.close()


    return {
        "id": new_id,
        "title": title,
        "done": False
    }





@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, updated_task: TaskUpdate):

    title = updated_task.title.strip()


    if not title:

        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (
            title,
            updated_task.done,
            task_id
        )
    )


    conn.commit()


    if cursor.rowcount == 0:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )


    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )


    row = cursor.fetchone()


    conn.close()


    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


@app.delete(
    "/tasks/{task_id}",
    summary="Delete a task",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )


    conn.commit()


    if cursor.rowcount == 0:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )


    conn.close()


    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )