import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid

def load_ignore_patterns(ignore_file):
    with open(ignore_file, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def should_ignore(file, patterns):
    return any(fnmatch.fnmatch(file, pattern) for pattern in patterns)

def get_file_type(file):
    ext = file.lower().split(".")[-1]
    if ext in ["svg"]:
        return "svg"
    if ext in ["png"]:
        return "png"
    if ext in ["jpg", "jpeg"]:
        return "jpg"
    if ext in ["webp"]:
        return "webp"
    if ext in ["gif"]:
        return "gif"
    if ext in ["pdf"]:
        return "pdf"
    return None

def process_file(file, file_type):
    temp_dir = tempfile.gettempdir()
    
    working_copy = file

    while True:
        temp_file = os.path.join(temp_dir, str(uuid.uuid4()))

        commands = {
            "svg": ["svgo", working_copy, "-o", temp_file],
            "png": ["pngquant", working_copy, "-o", temp_file],
            "jpg": ["jpegoptim", "--stdout", working_copy],
            "webp": ["cwebp", "-z", "9", working_copy, "-o", temp_file],
            "gif": ["gifsicle", "--optimize=3", "--output", temp_file, working_copy],
            "pdf": ["pdf2svg", working_copy, temp_file]
        }

        if file_type == "jpg":
            with open(temp_file, "wb") as out:
                result = subprocess.run(commands[file_type], stdout=out, stderr=subprocess.PIPE, check=False)
        else:
            result = subprocess.run(commands[file_type], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

        if result.returncode != 0:
            break

        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            break

        original_size = os.path.getsize(working_copy)
        optimized_size = os.path.getsize(temp_file)

        if optimized_size >= original_size:
            break

        working_copy = temp_file

        # Reprocess PDF as SVG
        if file_type == "pdf":
            file_type = "svg"
            continue

    if working_copy == file:
        return 0

    original_size = os.path.getsize(file)
    optimized_size = os.path.getsize(working_copy)

    if optimized_size >= original_size:
        return 0

    optimized_file = os.path.join("optim_guard_result", file)
    os.makedirs(os.path.dirname(optimized_file), exist_ok=True)
    shutil.move(working_copy, optimized_file)

    return original_size - optimized_size

def load_files_from_json(file_paths):
    files = []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            files.extend(json.load(f))
    return files

ignore_patterns = load_ignore_patterns(sys.argv[1])
files = load_files_from_json(sys.argv[2:])

total_reduced_bytes = 0

os.makedirs("optim_guard_result", exist_ok=True)

for file in files:
    if not file:
        continue

    if should_ignore(file, ignore_patterns):
        print(f"Ignoring: {file}")
        continue

    file_type = get_file_type(file)

    if not file_type:
        continue

    reduced_bytes = process_file(file, file_type)

    if reduced_bytes > 0:
        total_reduced_bytes += reduced_bytes

        if reduced_bytes < 1024:
            print(f"{file} | ❌ reduced {reduced_bytes} B")
        else:
            reduced_kb = reduced_bytes / 1024
            print(f"{file} | ❌ reduced {reduced_kb:.2f} kB")
    else:
        print(f"{file} | 👍")

if total_reduced_bytes > 0:
    total_reduced_kb = total_reduced_bytes / 1024
    print(f"Total reduced size: {total_reduced_kb:.2f} kB")
    print("Check job artefacts to download optimised files.")
    sys.exit(1)
