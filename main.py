from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

class PoemLine(BaseModel):
    agent_name: str
    line: str

class HubState:
    def __init__(self):
        self.poem: List[dict] = []
        self.is_running: bool = False

state = HubState()

# --- API Endpoints ---

@app.get("/api/hub")
def get_hub():
    return {"poem": state.poem, "is_running": state.is_running}

@app.post("/api/hub/line")
def add_line(entry: PoemLine):
    if not state.is_running:
        raise HTTPException(status_code=403, detail="Hub is currently stopped.")
    
    # Logic for default naming
    if not entry.agent_name or entry.agent_name.strip() == "":
        name = f"Agent {chr(65 + len(state.poem))}"
    else:
        name = entry.agent_name

    state.poem.append({"agent_name": name, "line": entry.line})
    return {"status": "success"}

@app.post("/api/hub/control")
def control_hub(action: str):
    if action == "start": state.is_running = True
    elif action == "end": state.is_running = False
    elif action == "reset":
        state.is_running = False
        state.poem = []
    return {"is_running": state.is_running}

# --- Frontend Routing ---

@app.get("/")
async def read_index():
    # Serves index.html from the root directory
    return FileResponse('index.html')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
