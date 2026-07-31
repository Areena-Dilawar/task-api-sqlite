# Task API (SQLite)

A simple RESTful Task Management API built with **FastAPI** and **SQLite** for the **FlyRank Backend Internship – Week 3 Assignment**.

## Features

* FastAPI framework
* SQLite database
* Full CRUD operations
* Automatic Swagger API documentation
* Input validation
* Proper HTTP status codes
* Parameterized SQL queries to prevent SQL injection

## Technologies Used

* Python 3.14
* FastAPI
* SQLite3
* Uvicorn

## Project Structure

```
task-api-sqlite/
│── main.py
│── tasks.db
│── requirements.txt
│── README.md
│── .gitignore
└── venv/
```

## Installation

Clone the repository:

```bash
git clone <your-github-repository-url>
```

Navigate to the project folder:

```bash
cd task-api-sqlite
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| GET    | `/`           | API information         |
| GET    | `/health`     | Health check            |
| GET    | `/tasks`      | Retrieve all tasks      |
| GET    | `/tasks/{id}` | Retrieve a task by ID   |
| POST   | `/tasks`      | Create a new task       |
| PUT    | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task           |

## Example Request

### Create Task

```http
POST /tasks
Content-Type: application/json
```

```json
{
  "title": "Learn SQLite"
}
```

## Example Response

```json
{
  "id": 4,
  "title": "Learn SQLite",
  "done": false
}
```

## Database

The application automatically:

* Creates `tasks.db` if it does not exist.
* Creates the `tasks` table.
* Inserts sample tasks only when the table is empty.

## HTTP Status Codes

* 200 OK
* 201 Created
* 204 No Content
* 400 Bad Request
* 404 Not Found

## Author

**Areena Dilawar**
