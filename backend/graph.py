from langgraph.graph import StateGraph, END

from agent_state import AgentState
from detect import detect_node
from understand import understand_node
from recommend import recommend_node
from respond import respond_node


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("detect", detect_node)
    graph.add_node("understand", understand_node)
    graph.add_node("recommend", recommend_node)
    graph.add_node("respond", respond_node)

    graph.set_entry_point("detect")

    graph.add_edge("detect", "understand")
    graph.add_edge("understand", "recommend")
    graph.add_edge("recommend", "respond")
    graph.add_edge("respond", END)

    return graph