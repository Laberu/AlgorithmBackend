import grpc
import algorithm_pb2
import algorithm_pb2_grpc
import os
import json
import time
from concurrent import futures
from dotenv import load_dotenv
from prometheus_client import start_http_server, Counter
from worker import WorkerPool, add_job  # ✅ Use WorkerPool & Queue

# ✅ Load .env variables
load_dotenv()

# ✅ Configurations from .env
STORAGE_PATH = os.getenv("STORAGE_PATH", "/app/storage")
GRPC_PORT = os.getenv("GRPC_PORT", "50051")
NUM_WORKERS = int(os.getenv("NUM_WORKERS", "4"))

# ✅ Prometheus Metrics
REQUEST_COUNT = Counter("backend_py_requests", "Total requests to backend-py")


class AlgorithmService(algorithm_pb2_grpc.AlgorithmServiceServicer):
    def UploadFile(self, request_iterator, context):
        """Receives file stream, saves it, and queues the job."""
        REQUEST_COUNT.inc()

        first_chunk = True
        job_id = None
        file_path = None
        with open("temp_file.zip", "wb") as f:
            for chunk in request_iterator:
                if first_chunk:
                    job_id = chunk.job_id
                    job_folder = os.path.join(STORAGE_PATH, job_id)
                    os.makedirs(job_folder, exist_ok=True)
                    file_path = os.path.join(job_folder, "input.zip")
                    f.close()
                    f = open(file_path, "wb")
                    first_chunk = False
                f.write(chunk.content)

        # ✅ Create `status.json`
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

        # ✅ Add job to the queue instead of starting immediately
        add_job(job_id, file_path)

        return algorithm_pb2.UploadResponse(job_id=job_id, status="queued")


    def GetJobStatus(self, request, context):
        """Returns the status of a given job ID"""
        job_id = request.job_id
        status_file = os.path.join(STORAGE_PATH, job_id, "status.json")

        print(f"status_file: {status_file}")

        if not os.path.exists(status_file):
            return algorithm_pb2.JobStatusResponse(
                job_id=job_id,
                status="not_found",
                progress=0,
                message="Job not found or not started yet."
            )

        with open(status_file, "r") as f:
            status_data = json.load(f)

        print(f"📄 Status file contents: {status_data}")

        return algorithm_pb2.JobStatusResponse(
            job_id=status_data.get("job_id", job_id),
            status=status_data.get("status", "unknown"),
            progress=status_data.get("progress", 0),
            message=status_data.get("message", "")
        )


    def DownloadFile(self, request, context):
        """Handles file download via gRPC."""
        job_id = request.job_id
        job_folder = os.path.join(STORAGE_PATH, job_id)
        output_zip = os.path.join(job_folder, "final_output.zip")

        # ✅ Check if the file exists
        if not os.path.exists(output_zip):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("File not found or job not completed yet.")
            return None

        # ✅ Read file in chunks
        def file_stream():
            with open(output_zip, "rb") as f:
                while chunk := f.read(4096):
                    yield algorithm_pb2.FileChunk(content=chunk)

        return file_stream()
    
    def ConfirmDelete(self, request, context):
        """Deletes job files after the client confirms the download."""
        job_id = request.job_id
        job_folder = os.path.join(STORAGE_PATH, job_id)

        if not os.path.exists(job_folder):
            return algorithm_pb2.ConfirmDeleteResponse(success=False, message="Job folder not found.")

        # ✅ Delete all files inside the folder
        for file in os.listdir(job_folder):
            file_path = os.path.join(job_folder, file)
            os.remove(file_path)

        # ✅ Remove the job folder
        os.rmdir(job_folder)

        print(f"🗑️ Job {job_id} files deleted upon confirmation.")
        return algorithm_pb2.ConfirmDeleteResponse(success=True, message="Job files deleted.")


def serve():
    start_http_server(8000)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    algorithm_pb2_grpc.add_AlgorithmServiceServicer_to_server(AlgorithmService(), server)
    server.add_insecure_port(f"[::]:{GRPC_PORT}")

    # ✅ Start Worker Pool
    global worker_pool
    worker_pool = WorkerPool(num_workers=NUM_WORKERS)

    print(f"🚀 gRPC Server running on port {GRPC_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
