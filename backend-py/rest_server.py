import os
import json
import shutil
import time
import uuid
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from worker import add_job  # ✅ Worker Queue for Processing
from prometheus_client import start_http_server

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Start Prometheus Metrics on Port 8000
start_http_server(8000)

# ✅ Storage Path
STORAGE_PATH = os.getenv("STORAGE_PATH", "/app/storage")

# ✅ Job Model
class JobStatus(BaseModel):
    job_id: str


def generate_job_id() -> str:
    """Generates a unique job ID using timestamp and UUID."""
    return f"{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Receives file via REST and queues it for processing with an auto-generated job ID."""
    job_id = generate_job_id()
    job_folder = os.path.join(STORAGE_PATH, job_id)
    os.makedirs(job_folder, exist_ok=True)

    file_path = os.path.join(job_folder, "input.zip")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Create status.json
    status_file = os.path.join(job_folder, "status.json")
    initial_status = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0,
        "message": "Job received, waiting for processing."
    }
    with open(status_file, "w") as f:
        json.dump(initial_status, f, indent=4)

    print(f"✅ Job {job_id} received. Status initialized.")

    # ✅ Add job to queue
    add_job(job_id, file_path)

    return {"job_id": job_id, "status": "queued"}


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Returns job processing status."""
    status_file = os.path.join(STORAGE_PATH, job_id, "status.json")

    if not os.path.exists(status_file):
        return {"job_id": job_id, "status": "not_found", "progress": 0, "message": "Job not found."}

    with open(status_file, "r") as f:
        status_data = json.load(f)

    return status_data


@app.get("/download/{job_id}")
async def download_file(job_id: str):
    """Handles file download via REST."""
    job_folder = os.path.join(STORAGE_PATH, job_id)
    output_zip = os.path.join(job_folder, "final_output.zip")

    if not os.path.exists(output_zip):
        return {"error": "File not found or job not completed yet."}

    return {"message": f"File available at {output_zip}"}


# ✅ Health Check Route
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ✅ Run API Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=50051)
