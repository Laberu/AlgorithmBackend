import time
import json
import os
import shutil

class MockAlgorithm:
    def __init__(self, input_zip: str, output_dir: str):
        """Initialize the mock algorithm with input zip file and output directory."""
        self.input_zip = input_zip
        self.output_dir = output_dir
        self.status_file = os.path.join(output_dir, "status.json")
        self.output_zip = os.path.join(output_dir, "final_output.zip")

    def update_status(self, status: str, progress: int, message: str):
        """Ensures the status.json file is properly updated."""
        status_data = {
            "job_id": os.path.basename(self.output_dir),
            "status": status,
            "progress": progress,
            "message": message
        }
        with open(self.status_file, "w") as f:
            json.dump(status_data, f, indent=4)
            
        print(f"algo status_file: {self.status_file}")
        print(f"📝 Status Updated: {status_data}")  # ✅ Debugging log

    def run(self):
        """Simulates a long-running process by updating progress every 15 seconds."""
        os.makedirs(self.output_dir, exist_ok=True)

        # ✅ Initial status
        self.update_status("processing", 0, "Job started. Processing...")

        # ✅ Simulate processing in intervals
        for i in range(1, 9):
            time.sleep(15)  # Wait 15 seconds
            progress = i * 12  # Progress increments (8 steps → 100%)
            self.update_status("processing", progress, f"Processing... {progress}% completed.")

        # ✅ Simulate final output file creation
        shutil.copy(self.input_zip, self.output_zip)  # Fake output
        self.update_status("completed", 100, "Job completed. Output is ready.")
        print(f"✅ Mock job completed: {self.output_zip}")
