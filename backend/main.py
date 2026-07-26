import asyncio
import random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from log_simulator import generate_log_entry
from detection_agent import detect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "AI SOC Agent backend is running"}

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            log = generate_log_entry()
            ai_result = detect(log)          # <-- real model prediction happens here
            log.update(ai_result)             # adds "ai_flagged" and "anomaly_score" to the log
            await websocket.send_json(log)
            await asyncio.sleep(random.uniform(0.5, 2))
    except Exception as e:
        print("Connection closed:", e)