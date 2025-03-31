import os
import uuid
import zipfile
import subprocess
import shutil
import json
import re
from algorithm.converter import convert_obj_to_fbx


class MeshroomReconstructor:
    def __init__(self, meshroom_bin=None):
        if meshroom_bin is None:
            meshroom_bin = os.getenv("MESHROOM_BIN")
        self.meshroom_bin = meshroom_bin
        if not os.path.exists(meshroom_bin):
            raise FileNotFoundError(f"Meshroom binary not found at: {meshroom_bin}")
        self.meshroom_bin = meshroom_bin
        self.total_steps = 12

    def _extract_zip(self, zip_path, working_dir):
        image_dir = os.path.join(working_dir, "images")
        os.makedirs(image_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(image_dir)
        return image_dir

    def _update_status(self, status_file, status, progress, message):
        status_data = {
            "status": status,
            "progress": progress,
            "message": message
        }
        with open(status_file, "w") as f:
            json.dump(status_data, f, indent=4)

    def _run_with_live_status(self, cmd, status_file):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        step_seen = set()

        for line in process.stdout:
            print(line.strip())
            match = re.search(r"\[(\d+)/(\d+)\]\s+([^\r\n]+)", line)
            if match:
                step = int(match.group(1))
                label = match.group(3)
                if step not in step_seen:
                    step_seen.add(step)
                    progress = int((step / self.total_steps) * 100)
                    self._update_status(status_file, "processing", progress, f"[{step}/{self.total_steps}] {label}")

        process.wait()
        return process.returncode

    def _create_data_json(self, output_folder):
        data_json = {
            "modelUrl": "model.fbx",
            "textureSets": {},
            "modelInfos": {
                "modelInfo": {
                    "name": "N/A",
                    "vertices": 0,
                    "faces": 0
                },
                "positions": []
            }
        }
        with open(os.path.join(output_folder, "data.json"), "w") as f:
            json.dump(data_json, f, indent=2, ensure_ascii=False)

    def _create_final_zip(self, output_dir, fbx_path, zip_path):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add FBX file as 'model.fbx'
            zipf.write(fbx_path, "model.fbx")
            # Add data.json
            data_json_path = os.path.join(output_dir, "data.json")
            if os.path.exists(data_json_path):
                zipf.write(data_json_path, "data.json")
            # Add empty texture folder (optional)
            texture_dir = os.path.join(output_dir, "texture")
            os.makedirs(texture_dir, exist_ok=True)
            for root, _, files in os.walk(texture_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, output_dir)
                    zipf.write(full_path, rel_path)

    def reconstruct(self, zip_path, output_base):
        working_dir = output_base
        os.makedirs(working_dir, exist_ok=True)
        status_file = os.path.join(working_dir, "status.json")
        self._update_status(status_file, "processing", 0, "Meshroom job started.")
        result_zip = os.path.join(working_dir, "final_output.zip")

        image_dir = self._extract_zip(zip_path, working_dir)
        output_dir = os.path.join(working_dir, "meshroom_output")
        os.makedirs(output_dir, exist_ok=True)

        cmd = [
            self.meshroom_bin,
            "--input", image_dir,
            "--output", output_dir,
            "--paramOverrides", "Texturing.textureSide=2048"
        ]

        try:
            returncode = self._run_with_live_status(cmd, status_file)
            if returncode != 0:
                raise subprocess.CalledProcessError(returncode, cmd)
        except subprocess.CalledProcessError as e:
            self._update_status(status_file, "failed", 100, f"Meshroom failed: {e}")
            return None

        obj_path = None
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith(".obj"):
                    obj_path = os.path.join(root, file)
                    break
            if obj_path:
                break

        fbx_path = os.path.join(output_dir, "model.fbx")
        if obj_path:
            try:
                convert_obj_to_fbx(obj_path, fbx_path)
            except Exception as e:
                print(f"[⚠️] FBX conversion failed: {e}")
                return None

        self._create_data_json(output_dir)
        self._create_final_zip(output_dir, fbx_path, result_zip)
        self._update_status(status_file, "completed", 100, "Reconstruction completed successfully.")
        return result_zip
