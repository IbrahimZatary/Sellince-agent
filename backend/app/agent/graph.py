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
    # If an offer is already established in state, proceed directly to respond
    if state.get("recommendation") or state.get("offer") or state.get("active_offer"):
        return "respond"

    intent_data = state.get("intent") or {}
    intent = intent_data.get("intent")
    needs = intent_data.get("needs", [])
    needs_str = " ".join(needs).lower()

    sales_keywords = ["upgrade", "buy", "offer", "purchase", "renew", "deal", "want"]

    # Recommend only if the user shows sales intent, has sales‑related needs, or
    # a trigger is relevant *and* the intent reflects a sales‑oriented action.
    # This prevents a generic trigger (e.g., usage‑based) from forcing a recommendation
    # when the user simply says hello.
    if (
        intent in ("accepts_offer", "ready_to_pay", "wants_details")
        or any(keyword in needs_str for keyword in sales_keywords)
        or (state.get("trigger_reason") is not None and intent in ("accepts_offer", "ready_to_pay", "wants_details"))
    ):
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