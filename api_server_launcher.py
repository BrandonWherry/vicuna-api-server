import subprocess
import threading


def run_controller():
    subprocess.run(
        ["python", "-m", "fastchat.serve.controller", "--host", "localhost"])


def run_model_worker():
    subprocess.run(
        ["python", "-m", "fastchat.serve.model_worker", "--host", "localhost", "--controller-address",
        "http://localhost:21001", "--model-path", "./vicuna-13b-v1.5-16k", "--load-8bit", "--device", "cpu"])


def run_api_server():
    subprocess.run(
        ["python", "-m", "fastchat.serve.openai_api_server", "--host",
        "localhost", "--controller-address", "http://localhost:21001", "--port", "8000"])


controller_thread = threading.Thread(target=run_controller)
controller_thread.start()

model_worker_thread = threading.Thread(target=run_model_worker)
model_worker_thread.start()

api_server_thread = threading.Thread(target=run_api_server)
api_server_thread.start()

""" For testing - CLI example of curl
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{ \
    "model": "vicuna-13b-v1.5-16k", \
    "messages": [{"role": "user", "content": "Hello, can you tell me a joke for me?"}], \
    "temperature": 0.5 \
  }'
"""
