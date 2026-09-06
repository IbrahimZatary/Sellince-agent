from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AppException, app_exception_handler
from app.api.auth import router as auth_router
from app.core.database import get_db
from graph import compiled_graph

app = FastAPI(title=settings.PROJECT_NAME)

app.add_exception_handler(AppException, app_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


class ChatRequest(BaseModel):
    customer_id: int = Field(..., gt=0)
    message: str = Field(..., min_length=1)


@app.post("/api/chat", status_code=status.HTTP_200_OK)
def chat_endpoint(payload: ChatRequest, db: Session = Depends(get_db)):
    initial_state = {
        "customer_id": payload.customer_id,
        "message": payload.message,
        "_db": db,
    }
    result = compiled_graph.invoke(initial_state)
    return {
        "response": result.get("response"),
        "offer": result.get("offer"),
        "action": result.get("action", "ask_question"),
    }
