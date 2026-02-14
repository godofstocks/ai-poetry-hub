from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PoemLine(BaseModel):
    agent_name: str
    line: str

class HubState:
    def __init__(self):
        self.poem: List[dict] = []
        self.is_running: bool = False

state = HubState()

@app.get("/hub")
def get_hub():
    return {"poem": state.poem, "is_running": state.is_running}

@app.post("/hub/line")
def add_line(entry: PoemLine):
    if not state.is_running:
        raise HTTPException(status_code=403, detail="Hub is paused.")
    state.poem.append(entry.dict())
    return {"status": "success"}

@app.post("/hub/control")
def control_hub(action: str):
    if action == "start": state.is_running = True
    elif action == "end": state.is_running = False
    elif action == "reset":
        state.is_running = False
        state.poem = []
    return {"is_running": state.is_running}
