import time
import json
import os
import shutil
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

class MockAlgorithm:
    def __init__(self, input_zip: str, output_dir: str):
        self.input_zip = input_zip
        self.output_dir = output_dir
        self.status_file = os.path.join(output_dir, "status.json")
        self.output_zip = os.path.join(output_dir, "final_output.zip")
        
        self.total_steps = 12
        self.total_time = int(os.getenv("DEMO_TOTAL_TIME", 180))  # Default: 180 seconds
        self.step_time = self.total_time / self.total_steps

    def update_status(self, status: str, progress: int, message: str):
        status_data = {
            "job_id": os.path.basename(self.output_dir),
            "status": status,
            "progress": progress,
            "message": message
        }
        with open(self.status_file, "w") as f:
            json.dump(status_data, f, indent=4)

        print(f"📝 Status Updated: {status_data}")

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)
        self.update_status("processing", 0, "Job started. Processing...")

        for i in range(1, self.total_steps + 1):
            time.sleep(self.step_time)
            progress = int((i / self.total_steps) * 100)
            self.update_status("processing", progress, f"Processing... {progress}% completed.")

        shutil.copy(self.input_zip, self.output_zip)
        self.update_status("completed", 100, "Job completed. Output is ready.")
        print(f"✅ Mock job completed: {self.output_zip}")
