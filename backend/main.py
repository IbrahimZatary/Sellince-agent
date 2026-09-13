from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.runner import run_agent_turn

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


class ChatRequest(BaseModel):
    customer_id: int
    conversation_id: int
    message: str


@app.post("/api/chat")
def chat(req: ChatRequest):
    result = run_agent_turn(
        conversation_id=req.conversation_id,
        state={
            "customer_id": req.customer_id,
            "message": req.message,
        },
    )

    recommendation = result.get("recommendation") or {}

    return {
        "response": result.get("response"),
        "offer": recommendation.get("primary"),
        "action": result.get("action"),
        "conversation_stage": result.get("conversation_stage"),
    }