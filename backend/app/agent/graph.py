from langgraph.graph import StateGraph, END

from app.agent.agent_state import AgentState
from app.agent.detect import detect_node
from app.agent.understand import understand_node
from app.agent.recommend import recommend_node
from app.agent.respond import respond_node

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

compiled_graph = graph.compile()
