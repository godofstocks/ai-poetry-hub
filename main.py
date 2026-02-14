from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

class PoemLine(BaseModel):
    agent_name: str
    line: str

class HubState:
    def __init__(self):
        self.poem: List[dict] = []
        self.is_running: bool = False

state = HubState()

# API Endpoints
@app.get("/api/hub")
def get_hub():
    return {"poem": state.poem, "is_running": state.is_running}

@app.post("/api/hub/line")
def add_line(entry: PoemLine):
    if not state.is_running:
        raise HTTPException(status_code=403, detail="Hub is closed.")
    
    # Auto-naming logic if name is empty
    if not entry.agent_name.strip():
        entry.agent_name = f"Agent {chr(65 + len(state.poem))}"
        
    state.poem.append(entry.dict())
    return {"status": "success"}

@app.post("/api/hub/control")
def control_hub(action: str):
    if action == "start": state.is_running = True
    elif action == "end": state.is_running = False
    elif action == "reset":
        state.is_running = False
        state.poem = []
    return {"is_running": state.is_running}

# Serve Static Files
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse('static/index.html')
