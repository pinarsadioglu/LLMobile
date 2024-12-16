import os
import subprocess
from apps.func import security_scans
import string
import random
import json


def is_apk(file):
    if not file.filename.lower().endswith('.apk'):
        return False
    return True

def generate_apk_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def AIAnalysis(file_path, apk_id):
    print("AI analyser has been started!")
    #apk_id = generate_apk_id()
    security_scans.initialize_ai(file_path, apk_id)

def decompile_apk(file_path, output_dir, apk_id):
    #command = ['apktool d', file_path, '-o', output_dir]
    print(output_dir)
    command = ['/home/sec/Desktop/jadx/bin/jadx', file_path, '-d', output_dir]

    try:
        print("Extracting...", command)
        #result = subprocess.run(command, check=True, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = subprocess.Popen(command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )
    
        # Çıktıları oku
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print("Extraction process has been finished successfuly...")
        else:
            print("Error:", stderr)

        AIAnalysis(file_path, apk_id)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode()}")

def run_semgrep(file_path):
    decompiled_apk_path = file_path[:-4]
    print(decompiled_apk_path)
    try:
        result = subprocess.run(
            ["semgrep", "--config", "auto", decompiled_apk_path, "--json", "--quiet", "--exclude", decompiled_apk_path+"/resources/AndroidManifest.xml"],
            capture_output=True,
            text=True
        )
        
        output = result.stdout
        errors = result.stderr
        
        if result.returncode == 0:
            output_json = json.loads(output)
            return json.dumps(output_json["results"])
        else:
            print({"status": "error", "output": output, "errors": errors})

    except Exception as e:
        print({"status": "error", "message": str(e)})


