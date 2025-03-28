import os
import json
import shutil
import time
import uuid
import threading
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from worker import WorkerPool, add_job  # ✅ Worker Queue for Processing
from prometheus_client import start_http_server
from fastapi.responses import FileResponse

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Start Prometheus Metrics on Port 8000
start_http_server(8000)

# ✅ Storage Path
STORAGE_PATH = os.getenv("STORAGE_PATH", "/app/storage")
NUM_WORKERS = int(os.getenv("NUM_WORKERS", "4"))  # Get from .env (Default 4 workers)

# ✅ Start Worker Pool (Important: This was missing before!)
worker_pool = WorkerPool(num_workers=NUM_WORKERS)


class JobStatus(BaseModel):
    job_id: str


def generate_job_id() -> str:
    """Generates a unique job ID using timestamp and UUID."""
    return f"{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Receives file via REST and queues it for processing with an auto-generated job ID."""
    try:
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


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
    """Handles file download via REST and updates status to finished."""
    job_folder = os.path.join(STORAGE_PATH, job_id)
    output_zip = os.path.join(job_folder, "final_output.zip")
    status_file = os.path.join(job_folder, "status.json")

    if not os.path.exists(output_zip):
        return {"error": "File not found or job not completed yet."}

    # ✅ Update status to finished
    if os.path.exists(status_file):
        try:
            with open(status_file, "r") as f:
                status_data = json.load(f)

            status_data["status"] = "finished"
            status_data["progress"] = 100
            status_data["message"] = "Download completed."

            with open(status_file, "w") as f:
                json.dump(status_data, f, indent=4)

            print(f"✅ Job {job_id} marked as finished after download.")

        except Exception as e:
            print(f"⚠️ Failed to update status for job {job_id}: {e}")

    return FileResponse(
        path=output_zip,
        filename=f"{job_id}_output.zip",
        media_type="application/zip"
    )


@app.get("/health")
def health_check():
    """Health Check Route"""
    return {"status": "healthy"}


# ✅ Run API Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=50051)
