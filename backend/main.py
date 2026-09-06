from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from graph import compiled_graph

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


class ChatRequest(BaseModel):
    customer_id: int
    message: str


@app.post("/api/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    result = compiled_graph.invoke({
        "customer_id": req.customer_id,
        "message": req.message,
        "_db": db,
    })
    return {
        "response": result["response"],
        "offer": result["recommendation"]["primary"] if result["recommendation"] else None,
        "action": result["action"],
    }