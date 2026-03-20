import os
import subprocess
import signal
import json
import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI(title="NexusLLM Dashboard API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
processes: Dict[str, subprocess.Popen] = {}

class TrainRequest(BaseModel):
    config: str
    deepspeed: bool = False

class ServeRequest(BaseModel):
    model_path: str
    port: int = 8000

@app.get("/status")
def get_status():
    return {
        "training": "active" if "train" in processes and processes["train"].poll() is None else "idle",
        "serving": "active" if "serve" in processes and processes["serve"].poll() is None else "idle"
    }

@app.post("/train/start")
def start_training(req: TrainRequest):
    if "train" in processes and processes["train"].poll() is None:
        raise HTTPException(status_code=400, detail="Training already in progress")
    
    cmd = ["python3", "nexus.py", "run", "train", "--config", req.config]
    if req.deepspeed:
        cmd.append("--deepspeed")
    
    # Run in background and redirect output to a log file
    log_file = open(os.path.join(PROJECT_ROOT, "outputs/training.log"), "w")
    processes["train"] = subprocess.Popen(
        cmd,
        cwd=PROJECT_ROOT,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid
    )
    return {"message": "Training started", "pid": processes["train"].pid}

@app.post("/train/stop")
def stop_training():
    if "train" not in processes or processes["train"].poll() is not None:
        return {"message": "No training process to stop"}
    
    os.killpg(os.getpgid(processes["train"].pid), signal.SIGTERM)
    return {"message": "Training stopped"}

@app.post("/serve/start")
def start_serving(req: ServeRequest):
    if "serve" in processes and processes["serve"].poll() is None:
        raise HTTPException(status_code=400, detail="Server already running")
    
    cmd = ["bash", "deployment/serve.sh", req.model_path, str(req.port)]
    processes["serve"] = subprocess.Popen(
        cmd,
        cwd=PROJECT_ROOT,
        preexec_fn=os.setsid
    )
    return {"message": "Server started", "pid": processes["serve"].pid}

@app.post("/serve/stop")
def stop_serving():
    if "serve" not in processes or processes["serve"].poll() is not None:
        return {"message": "No server to stop"}
    
    os.killpg(os.getpgid(processes["serve"].pid), signal.SIGTERM)
    return {"message": "Server stopped"}

@app.get("/configs")
def list_configs():
    config_dir = os.path.join(PROJECT_ROOT, "configs")
    configs = []
    for root, _, files in os.walk(config_dir):
        for f in files:
            if f.endswith(".yaml") or f.endswith(".json"):
                configs.append(os.path.relpath(os.path.join(root, f), config_dir))
    return configs

@app.websocket("/logs/training")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    log_path = os.path.join(PROJECT_ROOT, "outputs/training.log")
    
    # Ensure log file exists
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write("Waiting for training logs...\n")
            
    try:
        with open(log_path, "r") as f:
            # Go to end of file
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    await asyncio.sleep(0.5)
                    continue
                await websocket.send_text(line)
    except WebSocketDisconnect:
        print("Log WebSocket disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
