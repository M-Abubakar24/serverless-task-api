
import json
import unittest
from uuid import uuid4

from app.database import get_connection
from app.handler import lambda_handler


class TaskAPITests(unittest.TestCase):

    def setUp(self):
        """Start each test with an empty tasks table."""
        with get_connection() as connection:
            connection.execute("DELETE FROM tasks")

    def request(self, method, path, body=None):
        """Create a simulated API request."""
        event = {
            "httpMethod": method,
            "path": path,
            "body": json.dumps(body) if body is not None else None,
        }
        return lambda_handler(event, None)

    def test_list_tasks(self):
        result = self.request("GET", "/tasks")
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(json.loads(result["body"])["tasks"], [])

    def test_create_task(self):
        result = self.request(
            "POST",
            "/tasks",
            {"title": "Learn AWS and Azure"},
        )

        self.assertEqual(result["statusCode"], 201)
        task = json.loads(result["body"])["task"]
        self.assertEqual(task["title"], "Learn AWS and Azure")
        self.assertFalse(task["completed"])

    def test_create_task_without_title(self):
        result = self.request("POST", "/tasks", {})
        self.assertEqual(result["statusCode"], 400)

    def test_get_task(self):
        task_id = str(uuid4())

        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO tasks (id, title, description, completed)
                VALUES (?, ?, ?, ?)
                """,
                (task_id, "Test task", "Test description", 0),
            )

        result = self.request("GET", f"/tasks/{task_id}")
        self.assertEqual(result["statusCode"], 200)

        task = json.loads(result["body"])["task"]
        self.assertEqual(task["id"], task_id)
        self.assertEqual(task["title"], "Test task")

    def test_update_task(self):
        task_id = str(uuid4())

        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO tasks (id, title, description, completed)
                VALUES (?, ?, ?, ?)
                """,
                (task_id, "Old title", "", 0),
            )

        result = self.request(
            "PATCH",
            f"/tasks/{task_id}",
            {"completed": True},
        )

        self.assertEqual(result["statusCode"], 200)
        task = json.loads(result["body"])["task"]
        self.assertTrue(task["completed"])

    def test_delete_task(self):
        task_id = str(uuid4())

        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO tasks (id, title, description, completed)
                VALUES (?, ?, ?, ?)
                """,
                (task_id, "Delete me", "", 0),
            )

        result = self.request("DELETE", f"/tasks/{task_id}")
        self.assertEqual(result["statusCode"], 200)

        result = self.request("GET", f"/tasks/{task_id}")
        self.assertEqual(result["statusCode"], 404)

    def test_get_missing_task(self):
        result = self.request("GET", f"/tasks/{uuid4()}")
        self.assertEqual(result["statusCode"], 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
