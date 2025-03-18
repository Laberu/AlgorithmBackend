import os
import queue
import threading
import json
import time
from prometheus_client import Gauge, Counter, Histogram
from algorithm.mock_algorithm import MockAlgorithm

job_queue = queue.Queue()

# ✅ Prometheus Metrics
job_queue_length = Gauge("job_queue_length", "Number of jobs waiting in the queue")
active_workers = Gauge("active_workers", "Number of active worker threads")
completed_jobs = Counter("completed_jobs", "Total completed jobs")
job_processing_time = Histogram("job_processing_time_seconds", "Time taken for each job", ["job_id"])

class WorkerPool:
    def __init__(self, num_workers=4):
        self.num_workers = num_workers
        self.workers = []
        self.stop_event = threading.Event()

        for _ in range(self.num_workers):
            worker_thread = threading.Thread(target=self.worker_loop, daemon=True)
            worker_thread.start()
            self.workers.append(worker_thread)

    def worker_loop(self):
        """Worker function that continuously processes jobs from the queue."""
        while not self.stop_event.is_set():
            try:
                job_id, input_zip, output_dir = job_queue.get(timeout=1)
                job_queue_length.set(job_queue.qsize())  # Update queue length
                active_workers.inc()  # Increment active worker count
                
                print(f"🚀 Worker processing job {job_id}")
                start_time = time.time()  # Track processing start time
                
                self.process_job(job_id, input_zip, output_dir)

                duration = time.time() - start_time  # Calculate processing time
                job_processing_time.labels(job_id=job_id).observe(duration)  # Track processing time
                
                print(f"✅ Job {job_id} finished in {duration:.2f} seconds")
                completed_jobs.inc()  # Update completed job metric

            except queue.Empty:
                continue  # No jobs, keep waiting

            finally:
                active_workers.dec()  # Decrement active workers when done

    def process_job(self, job_id, input_zip, output_dir):
        """✅ Uses `mocking_algorithm` for processing."""
        os.makedirs(output_dir, exist_ok=True)

        # ✅ Run the Mocking Algorithm
        mock_algo = MockAlgorithm(input_zip, output_dir)
        mock_algo.run()

        # ✅ Ensure the final status is written properly
        time.sleep(1)  # Small delay to allow filesystem sync
        status_file = os.path.join(output_dir, "status.json")
        if os.path.exists(status_file):
            with open(status_file, "r") as f:
                final_status = json.load(f)

                print(f"worker status_file: {status_file}")
                print(f"📜 Final Status: {final_status}")  # ✅ Debugging log

    def stop_workers(self):
        """Stop all worker threads cleanly."""
        self.stop_event.set()
        for worker in self.workers:
            worker.join()


# ✅ Function to add jobs to the queue
def add_job(job_id, input_zip):
    job_folder = os.path.join("/app/storage", job_id)
    job_queue.put((job_id, input_zip, job_folder))
    job_queue_length.set(job_queue.qsize())  # Update Prometheus metric
