from functools import wraps
import os
import uuid
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

AUTH_TOKEN = os.environ.get("WORKER_AUTH_TOKEN")

jobs = {} # Temporary in-memory dictionary to save (UUID, internalID), testing

def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header[len("Bearer "):].strip()

        if token != AUTH_TOKEN:
            return jsonify({"error": "Invalid token"}), 403
        
        return f(*args, **kwargs)
    return decorator


@app.route("/create/", methods=["POST"])
@auth_required
def job_create():
    # TO-DO, create the job logic
    
    job_uuid = str(uuid.uuid4())
    internal_id = random.randint(1,10) # Just to test the storage, this is the internal rclone job ID
    
    jobs[job_uuid] = internal_id
    
    return jsonify({
        "job_uuid": job_uuid,
        "status": "created"
    }), 201

@app.route("/query/", methods=["GET"])
@auth_required
def job_query():
    job_uuid = request.headers.get("jobUUID")
    
    if not job_uuid in jobs:
        return jsonify({"error": "Job not found"}), 404
    
    internal_id = jobs[job_uuid]
    jobs.pop(job_uuid)  # Remove after querying
    
    return jsonify({
        "job_uuid": job_uuid,
        "internal_id": internal_id,
        "status": "completed"
    }), 200
    
