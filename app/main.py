from functools import wraps
import os
from flask import Flask, request, abort

app = Flask(__name__)

AUTH_TOKEN = os.environ.get("WORKER_AUTH_TOKEN")

def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            abort(401, description="Missing or invalid Authorization header")

        token = auth_header[len("Bearer "):].strip()

        if token != AUTH_TOKEN:
            abort(403, description="Invalid token")
        
        return f(*args, **kwargs)
    return decorator


@app.route("/", methods=["POST"])
@auth_required
def hello():
    return "Hello World"
