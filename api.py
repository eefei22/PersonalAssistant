import os
import secrets
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

load_dotenv(Path(__file__).parent / "configs" / "config.env")

from agent.agent import run_agent

app = FastAPI(title="Personal Assistant API")

# ---------------------------------------------------------------------------
# Auth — simple API key check via X-API-Key header
# ---------------------------------------------------------------------------

API_KEY = os.environ["PA_API_KEY"]
api_key_header = APIKeyHeader(name="X-API-Key")


def verify_key(key: str = Security(api_key_header)) -> str:
    if not secrets.compare_digest(key, API_KEY):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key


# ---------------------------------------------------------------------------
# Session store — keeps conversation history per session_id in memory
# ---------------------------------------------------------------------------

sessions: dict[str, list] = {}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, _: str = Security(verify_key)):
    if req.session_id not in sessions:
        sessions[req.session_id] = []

    reply = run_agent(req.message, sessions[req.session_id])
    return ChatResponse(reply=reply, session_id=req.session_id)


@app.delete("/session/{session_id}")
def clear_session(session_id: str, _: str = Security(verify_key)):
    sessions.pop(session_id, None)
    return {"cleared": session_id}


@app.get("/health")
def health():
    return {"status": "ok"}
