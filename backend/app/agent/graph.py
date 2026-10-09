from langgraph.graph import StateGraph, END
from app.agent.agent_state import AgentState
from app.agent.detect import detect_node
from app.agent.understand import understand_node
from app.agent.recommend import recommend_node
from app.agent.respond import respond_node
from langgraph.checkpoint.memory import MemorySaver

def route_after_understand(state: AgentState):
    # Extract the dictionary of intents from the state
    intent_data = state.get("intent") or {}
    needs = intent_data.get("needs", [])
    
    # Convert all needs to a single lowercase string for easy checking
    needs_str = " ".join(needs).lower()
    
    # Check if the user explicitly wants an upgrade or offer
    sales_keywords = ["upgrade", "buy", "offer", "purchase", "renew", "deal"]
    
    # If the ONLY need detected was from a complaint like "slow", 
    # we want to handle it in support (respond), not sales (recommend)
    if any(keyword in needs_str for keyword in sales_keywords):
        return "recommend"
    
    # Default to customer support and general chat
    return "respond"

workflow = StateGraph(AgentState)

workflow.add_node("detect", detect_node)
workflow.add_node("understand", understand_node)
workflow.add_node("recommend", recommend_node)
workflow.add_node("respond", respond_node)

workflow.set_entry_point("detect")
workflow.add_edge("detect", "understand")

workflow.add_conditional_edges(
    "understand",
    route_after_understand,
    {
        "recommend": "recommend",
        "respond": "respond"
    }
)

workflow.add_edge("recommend", "respond")
workflow.add_edge("respond", END)

memory = MemorySaver()
compiled_graph = workflow.compile(checkpointer=memory)
