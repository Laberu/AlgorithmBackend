import os
import subprocess
import sys

def convert_obj_to_fbx(obj_path, fbx_path, blender_path=None):
    if blender_path is None:
        blender_path = os.getenv("BLENDER_PATH")
    if not os.path.exists(blender_path):
        raise FileNotFoundError(f"❌ Blender not found at: {blender_path}")
    if not os.path.exists(obj_path):
        raise FileNotFoundError(f"❌ OBJ file not found: {obj_path}")

    # Create temporary Blender script to handle conversion
    script_content = f"""
import bpy
import sys

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print('[Blender] Importing OBJ: {obj_path}')
bpy.ops.wm.obj_import(filepath=r'{obj_path}')

print('[Blender] Exporting FBX: {fbx_path}')
bpy.ops.export_scene.fbx(filepath=r'{fbx_path}', use_selection=False)
"""

    temp_script_path = "blender_convert_temp.py"
    with open(temp_script_path, "w") as f:
        f.write(script_content)

    print(f"[⚙️] Running Blender to convert:\n  OBJ: {obj_path}\n  FBX: {fbx_path}")
    subprocess.run([
        blender_path,
        "--background",
        "--python", temp_script_path
    ], check=True)

    os.remove(temp_script_path)
    print("[✅] Conversion complete.")

# -------------------------------
# 🔧 Run directly from terminal
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python converter.py input.obj output.fbx")
        sys.exit(1)

    input_obj = sys.argv[1]
    output_fbx = sys.argv[2]
    convert_obj_to_fbx(input_obj, output_fbx)
