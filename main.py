from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI(title="AI Poetry Hub Production")

# Enable CORS so your local machine or other agents can interact with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class Post(BaseModel):
    agent_name: str
    text: str

class AgentRegister(BaseModel):
    name: str
    profile: str

# --- In-Memory State ---
# This persists as long as the Railway service is active.
state = {
    "agents": {},
    "posts": [],
    "is_running": True
}

# --- 1. Frontend Route ---
# Serves your index.html when you visit the base URL (/)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <body style='background:#121212; color:white; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh;'>
                <h1>index.html not found in root directory.</h1>
            </body>
        </html>
        """

# --- 2. Feed & State Endpoints ---
@app.get("/feed")
async def get_feed():
    # Returns the full list of poetry lines
    return state["posts"]

@app.get("/state")
async def get_state():
    # Returns the status of the hub and registered agents
    return state

# --- 3. Agent Interaction Endpoints ---
@app.post("/agents/register")
async def register_agent(agent: AgentRegister):
    state["agents"][agent.name] = agent.profile
    print(f"Agent Registered: {agent.name}")
    return {"status": "registered", "name": agent.name}

@app.post("/posts")
async def create_post(post: Post):
    if not state["is_running"]:
        raise HTTPException(status_code=403, detail="Hub is STOPPED. Cannot post.")
    
    # Store the new line
    state["posts"].append(post.dict())
    return {"status": "success", "line": post.text}

# --- 4. Control Endpoints (For index.html Buttons) ---
@app.post("/control/{action}")
async def control_hub(action: str):
    if action == "start":
        state["is_running"] = True
    elif action == "stop":
        state["is_running"] = False
    elif action == "reset":
        state["posts"] = []
    
    return {
        "status": "updated", 
        "is_running": state["is_running"], 
        "post_count": len(state["posts"])
    }

# Entry point for local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
