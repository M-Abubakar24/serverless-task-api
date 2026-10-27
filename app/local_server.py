
from http.server import BaseHTTPRequestHandler, HTTPServer

from app.handler import lambda_handler


class TaskAPIHandler(BaseHTTPRequestHandler):

    def handle_request(self):
        # Read the request body, if present.
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        # Convert the HTTP request into a Lambda-style event.
        event = {
            "httpMethod": self.command,
            "path": self.path.split("?")[0],
            "body": body,
        }

        # Run our existing API handler.
        result = lambda_handler(event, None)

        # Send the handler's response to the HTTP client.
        response_body = result["body"].encode("utf-8")

        self.send_response(result["statusCode"])

        for name, value in result.get("headers", {}).items():
            self.send_header(name, value)

        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    do_GET = handle_request
    do_POST = handle_request
    do_PATCH = handle_request
    do_PUT = handle_request
    do_DELETE = handle_request


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), TaskAPIHandler)

    print("Task API running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
