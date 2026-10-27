
import json
from uuid import uuid4

from app.database import get_connection, row_to_task


def response(status_code, data):
    """Build a JSON HTTP response."""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data),
    }


def parse_body(event):
    """Parse and validate a JSON request body."""
    try:
        body = event.get("body") or "{}"

        if isinstance(body, str):
            body = json.loads(body)

        if not isinstance(body, dict):
            return None, response(400, {
                "error": "Request body must be a JSON object"
            })

        return body, None

    except (json.JSONDecodeError, TypeError):
        return None, response(400, {
            "error": "Invalid JSON request body"
        })


def lambda_handler(event, context):
    """Handle Task Management API requests using SQLite."""

    method = (
        event.get("httpMethod")
        or event.get("requestContext", {})
        .get("http", {})
        .get("method")
        or "GET"
    ).upper()

    path = event.get("path") or event.get("rawPath") or "/"
    path = path.rstrip("/") or "/"
    parts = path.strip("/").split("/") if path != "/" else []

    if not parts or parts[0] != "tasks":
        return response(404, {"error": "Route not found"})

    # GET /tasks — list all tasks
    if len(parts) == 1 and method == "GET":
        connection = get_connection()
        try:
            rows = connection.execute(
                "SELECT * FROM tasks ORDER BY rowid"
            ).fetchall()

            return response(200, {
                "message": "Tasks retrieved successfully",
                "tasks": [row_to_task(row) for row in rows],
            })
        finally:
            connection.close()

    # POST /tasks — create a task
    if len(parts) == 1 and method == "POST":
        body, error = parse_body(event)
        if error:
            return error

        title = body.get("title")
        if not isinstance(title, str) or not title.strip():
            return response(400, {
                "error": "A non-empty title is required"
            })

        description = body.get("description", "")
        if not isinstance(description, str):
            return response(400, {
                "error": "Description must be a string"
            })

        task = {
            "id": str(uuid4()),
            "title": title.strip(),
            "description": description,
            "completed": False,
        }

        connection = get_connection()
        try:
            connection.execute(
                """
                INSERT INTO tasks (id, title, description, completed)
                VALUES (?, ?, ?, ?)
                """,
                (
                    task["id"],
                    task["title"],
                    task["description"],
                    0,
                ),
            )
            connection.commit()
        finally:
            connection.close()

        return response(201, {
            "message": "Task created successfully",
            "task": task,
        })

    # Routes for an individual task: /tasks/{task_id}
    if len(parts) == 2:
        task_id = parts[1]

        if method == "GET":
            connection = get_connection()
            try:
                row = connection.execute(
                    "SELECT * FROM tasks WHERE id = ?",
                    (task_id,),
                ).fetchone()
                task = row_to_task(row)
            finally:
                connection.close()

            if task is None:
                return response(404, {"error": "Task not found"})

            return response(200, {"task": task})

        # PUT or PATCH /tasks/{task_id}
        if method in ("PUT", "PATCH"):
            body, error = parse_body(event)
            if error:
                return error

            connection = get_connection()
            try:
                row = connection.execute(
                    "SELECT * FROM tasks WHERE id = ?",
                    (task_id,),
                ).fetchone()

                task = row_to_task(row)

                if task is None:
                    return response(404, {"error": "Task not found"})

                if "title" in body:
                    title = body["title"]
                    if not isinstance(title, str) or not title.strip():
                        return response(400, {
                            "error": "Title must be a non-empty string"
                        })
                    task["title"] = title.strip()

                if "description" in body:
                    if not isinstance(body["description"], str):
                        return response(400, {
                            "error": "Description must be a string"
                        })
                    task["description"] = body["description"]

                if "completed" in body:
                    if not isinstance(body["completed"], bool):
                        return response(400, {
                            "error": "Completed must be true or false"
                        })
                    task["completed"] = body["completed"]

                connection.execute(
                    """
                    UPDATE tasks
                    SET title = ?, description = ?, completed = ?
                    WHERE id = ?
                    """,
                    (
                        task["title"],
                        task["description"],
                        int(task["completed"]),
                        task_id,
                    ),
                )
                connection.commit()
            finally:
                connection.close()

            return response(200, {
                "message": "Task updated successfully",
                "task": task,
            })

        # DELETE /tasks/{task_id}
        if method == "DELETE":
            connection = get_connection()
            try:
                cursor = connection.execute(
                    "DELETE FROM tasks WHERE id = ?",
                    (task_id,),
                )
                connection.commit()

                if cursor.rowcount == 0:
                    return response(404, {"error": "Task not found"})
            finally:
                connection.close()

            return response(200, {
                "message": "Task deleted successfully"
            })

        return response(405, {"error": "Method not allowed"})

    return response(404, {"error": "Route not found"})
