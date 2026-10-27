
from flask import Flask, request, Response
import json

from app.handler import lambda_handler

app = Flask(__name__)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def handle_request(path):
    event = {
        "httpMethod": request.method,
        "path": request.path,
        "headers": dict(request.headers),
        "queryStringParameters": request.args.to_dict() or None,
        "body": request.get_data(as_text=True) or None,
    }

    result = lambda_handler(event, None)

    return Response(
        response=result.get("body", ""),
        status=result.get("statusCode", 200),
        headers=result.get("headers", {}),
    )
