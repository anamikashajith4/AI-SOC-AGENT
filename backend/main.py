import asyncio
import random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from log_simulator import generate_log_entry

app = FastAPI()

# Allow our future React frontend (running on a different port) to connect
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
            await websocket.send_json(log)
            await asyncio.sleep(random.uniform(0.5, 2))
    except Exception as e:
        print("Connection closed:", e)