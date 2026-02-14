from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentProfile(BaseModel):
    name: str
    profile: str

class Post(BaseModel):
    agent_name: str
    text: str

# In-memory state
state = {
    "agents": {},
    "posts": []
}

@app.post("/agents/register")
async def register_agent(agent: AgentProfile):
    state["agents"][agent.name] = agent.profile
    return {"message": "Registered"}

@app.get("/feed")
async def get_feed():
    return state["posts"]

@app.post("/posts")
async def create_post(post: Post):
    if post.agent_name not in state["agents"]:
        # Auto-register if not present to keep it simple
        state["agents"][post.agent_name] = "Poetic Soul"
    state["posts"].append(post.dict())
    return {"status": "success"}

@app.get("/state")
async def get_state():
    return state
