import os
from flask import Flask, send_from_directory, request, jsonify
from threading import Thread
import subprocess

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/run_gesture', methods=['POST'])
def run_gesture():
    def gesture_worker():
        script_path = os.path.join(os.path.dirname(__file__), "inference_classifier.py")
        subprocess.Popen(["python", script_path])
    Thread(target=gesture_worker).start()
    return jsonify({"status": "started"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
