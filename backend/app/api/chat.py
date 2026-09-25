from fastapi import APIRouter, status
from app.schemas.chat import ChatRequest, ChatResponse
from app.agent.graph import compiled_graph

router = APIRouter(tags=["Chat"])

@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chat_endpoint(payload: ChatRequest):
    initial_state = {
        "customer_id": payload.customer_id,
        "message": payload.message,
    }
    
    result = compiled_graph.invoke(
        initial_state,
        config={"configurable": {"thread_id": str(payload.customer_id)}}
    )
    
    return {
        "response": result.get("response"),
        "offer": result.get("offer"),
        "action": result.get("action", "ask_question"),
        "action_payload": result.get("action_payload"),
    }
