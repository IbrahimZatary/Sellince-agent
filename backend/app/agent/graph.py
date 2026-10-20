
from langgraph.graph import StateGraph, START, END

from app.agent.agent_state import AgentState
from app.agent.detect import detect_node
from app.agent.understand import understand_node
from app.agent.recommend import recommend_node
from app.agent.respond import respond_node
from app.agent.proactive import proactive_offer_node


def route_entry(state: AgentState) -> str:
    if state.get("entry_type") == "proactive":
        return "proactive"

    return "detect"


def route_after_detect(state: AgentState) -> str:
    if state.get("customer_data") is None:
        return "respond"

    return "understand"


def build_graph():
    graph = StateGraph(AgentState)

    # Existing Agent Nodes
    graph.add_node("detect", detect_node)
    graph.add_node("understand", understand_node)
    graph.add_node("recommend", recommend_node)
    graph.add_node("respond", respond_node)

    # New Proactive Agent Node
    graph.add_node("proactive", proactive_offer_node)

    # Choose entry based on request type
    graph.add_conditional_edges(
        START,
        route_entry,
        {
            "proactive": "proactive",
            "detect": "detect",
        },
    )

    # Existing conversation flow
    graph.add_conditional_edges(
        "detect",
        route_after_detect,
        {
            "understand": "understand",
            "respond": "respond",
        },
    )

    graph.add_edge("understand", "recommend")
    graph.add_edge("recommend", "respond")
    graph.add_edge("respond", END)

    # Proactive flow stops after generating opening message
    graph.add_edge("proactive", END)

    return graph
