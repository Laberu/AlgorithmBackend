import os
import threading
import time
from prometheus_client import start_http_server, Gauge
from algorithm.mock_algorithm import MockAlgorithm
from dotenv import load_dotenv

load_dotenv()

STORAGE_PATH = os.getenv("STORAGE_PATH", "/app/storage")

# Prometheus Metrics
queue_length = Gauge("job_queue_length", "Number of jobs waiting in the queue")
active_workers = Gauge("active_workers", "Number of active worker threads")
completed_jobs = Gauge("completed_jobs", "Total completed jobs")

# **Queue for Jobs**
job_queue = queue.Queue()

class BackgroundWorker:
    def __init__(self):
        self.jobs = {}
        start_http_server(9091)  # Start metrics server for Prometheus

    def start_job(self, job_id: str, input_zip: str):
        """
        Starts a background thread to run the mock algorithm.
        """
        output_dir = os.path.join(STORAGE_PATH, job_id)

        # Define a wrapper function to run in a separate thread
        def run_algorithm():
            global active_threads, completed_jobs
            active_threads.inc()  # Increase active threads count
            print(f"🚀 Starting job {job_id}")

            algorithm = MockAlgorithm(input_zip, output_dir)
            algorithm.run()

            active_threads.dec()  # Decrease after completion
            completed_jobs.inc()  # Increase completed jobs count
            print(f"✅ Job {job_id} finished")

        # Start a new thread for the job
        job_thread = threading.Thread(target=run_algorithm)
        job_thread.start()

        # Store thread reference (optional for tracking)
        self.jobs[job_id] = job_thread

worker = BackgroundWorker()
