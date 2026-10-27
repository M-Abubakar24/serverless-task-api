# Serverless Task Management API

A Python-based REST API for managing tasks, built to practice serverless-style backend development, CRUD operations, database integration, and cloud deployment.

## 🚀 Live Demo

- **Live API:** https://abubakar.pythonanywhere.com
- **Get All Tasks:** https://abubakar.pythonanywhere.com/tasks
- **GitHub Repository:** https://github.com/M-Abubakar24/serverless-task-api

## 📌 Features

- Create new tasks
- Retrieve all tasks
- Retrieve an individual task by ID
- Update existing tasks
- Delete tasks
- Store task data using SQLite
- Return JSON responses
- Handle HTTP requests through a Flask web adapter
- Deploy a Python API to a public hosting platform

## 🛠️ Tech Stack

- **Language:** Python
- **Web Framework:** Flask
- **API Architecture:** REST
- **Database:** SQLite
- **Web Server:** Gunicorn
- **Testing:** Python `unittest`
- **Hosting:** PythonAnywhere
- **Version Control:** Git and GitHub

## 📂 Project Structure

```text
serverless-task-api/
├── app/
│   ├── __init__.py
│   ├── handler.py
│   ├── database.py
│   ├── local_server.py
│   └── render_server.py
├── test_handler.py
├── requirements.txt
└── .gitignore
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks` | Retrieve all tasks |
| POST | `/tasks` | Create a task |
| GET | `/tasks/{id}` | Retrieve a task by ID |
| PATCH | `/tasks/{id}` | Update a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

### 1. Retrieve All Tasks

**Request**

```http
GET /tasks
```

**Example response**

```json
{
  "message": "Tasks retrieved successfully",
  "tasks": [
    {
      "id": "example-task-id",
      "title": "Learn Python",
      "description": "Practice REST API development",
      "completed": false
    }
  ]
}
```

### 2. Create a Task

**Request**

```http
POST /tasks
Content-Type: application/json
```

**Example request body**

```json
{
  "title": "Learn API Deployment",
  "description": "Deploy a Python REST API",
  "completed": false
}
```

### 3. Retrieve a Single Task

**Request**

```http
GET /tasks/{id}
```

Replace `{id}` with the ID of an existing task.

### 4. Update a Task

**Request**

```http
PATCH /tasks/{id}
Content-Type: application/json
```

**Example request body**

```json
{
  "title": "Learn API Deployment",
  "completed": true
}
```

### 5. Delete a Task

**Request**

```http
DELETE /tasks/{id}
```

Replace `{id}` with the ID of the task you want to delete.

## 💻 Run Locally

### Prerequisites

- Python 3.10 or another compatible Python version
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/M-Abubakar24/serverless-task-api.git
cd serverless-task-api
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the local server

```bash
python -m app.local_server
```

Open the following URL in your browser:

http://127.0.0.1:8000/tasks

## 🧪 Run Tests

Run the unit test suite with:

```bash
python -m unittest test_handler -v
```

## ☁️ Deployment

The API is hosted on PythonAnywhere and can be accessed publicly.

**Deployment URL:** https://abubakar.pythonanywhere.com

The application uses a WSGI configuration to expose the Flask adapter and serve HTTP requests through the hosting platform.

## 🗄️ Database

The project uses SQLite to store task records, including:

- Task ID
- Title
- Description
- Completion status

**Note:** SQLite database files are local to the deployed application environment. Back up important data and verify the host's storage persistence before relying on production data.

## 🎯 Learning Objectives

This project demonstrates practical experience with:

- Designing RESTful API endpoints
- Implementing CRUD operations
- Handling JSON requests and responses
- Integrating a relational database
- Writing unit tests
- Using Git and GitHub for version control
- Deploying a Python application to a public hosting platform

## 🔮 Future Improvements

- Add authentication and user-specific tasks
- Add input validation and consistent error handling
- Add automated API tests
- Introduce PostgreSQL for more robust persistent storage
- Add CI/CD with GitHub Actions
- Add API documentation using Swagger or OpenAPI
- Add logging, monitoring, and rate limiting

## 👨‍💻 Author

**Muhammad Abubakar**

Software Engineering Graduate | Backend Development | REST APIs | Python

- **GitHub:** https://github.com/M-Abubakar24
- **Live Project:** https://abubakar.pythonanywhere.com

---

If you find this project useful, consider giving the repository a ⭐ on GitHub.
