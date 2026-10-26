from langgraph.graph import StateGraph, START, END

from app.agent.agent_state import AgentState
from app.agent.detect import detect_node
from app.agent.understand import understand_node
from app.agent.recommend import recommend_node
from app.agent.respond import respond_node
from app.agent.proactive import proactive_offer_node


def route_after_detect(state: AgentState) -> str:
    proactive = state.get("entry_type") == "proactive"

    if state.get("customer_data") is None:
        # Nobody to talk to: a proactive session simply ends.
        return "end" if proactive else "respond"

    # Proactive sessions have no customer message to understand.
    return "recommend" if proactive else "understand"


def route_after_understand(state: AgentState):
    # Extract the dictionary of intents from the state
    intent_data = state.get("intent") or {}
    needs = intent_data.get("needs", [])

    # Convert all needs to a single lowercase string for easy checking
    needs_str = " ".join(needs).lower()

    # Check if the user explicitly wants an upgrade or offer
    sales_keywords = ["upgrade", "buy", "offer", "purchase", "renew", "deal"]

    # If the only need detected was from a complaint like "slow",
    # handle it in support (respond), not sales (recommend)
    if any(keyword in needs_str for keyword in sales_keywords):
        return "recommend"

    # Default to customer support and general chat
    return "respond"

def route_after_recommend(state: AgentState) -> str:
    if state.get("entry_type") == "proactive":
        return "proactive"

    return "respond"


def build_graph():
    graph = StateGraph(AgentState)

    # Existing Agent Nodes
    graph.add_node("detect", detect_node)
    graph.add_node("understand", understand_node)
    graph.add_node("recommend", recommend_node)
    graph.add_node("respond", respond_node)

    # New Proactive Agent Node
    graph.add_node("proactive", proactive_offer_node)

    # Every session starts by detecting the customer and their trigger.
    graph.add_edge(START, "detect")

    # Existing conversation flow
    graph.add_conditional_edges(
        "detect",
        route_after_detect,
        {
            "understand": "understand",
            "recommend": "recommend",
            "respond": "respond",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "understand",
        route_after_understand,
        {
            "recommend": "recommend",
            "respond": "respond",
        },
    )

    graph.add_conditional_edges(
        "recommend",
        route_after_recommend,
        {
            "proactive": "proactive",
            "respond": "respond",
        },
    )

    graph.add_edge("respond", END)

    # Proactive flow stops after composing the opening message
    graph.add_edge("proactive", END)

    return graph