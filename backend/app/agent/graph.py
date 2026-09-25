from langgraph.graph import StateGraph, END
from app.agent.agent_state import AgentState
from app.agent.detect import detect_node
from app.agent.understand import understand_node
from app.agent.recommend import recommend_node
from app.agent.respond import respond_node
from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(AgentState)

workflow.add_node("detect", detect_node)
workflow.add_node("understand", understand_node)
workflow.add_node("recommend", recommend_node)
workflow.add_node("respond", respond_node)

workflow.set_entry_point("detect")
workflow.add_edge("detect", "understand")
workflow.add_edge("understand", "recommend")
workflow.add_edge("recommend", "respond")
workflow.add_edge("respond", END)

memory = MemorySaver()
compiled_graph = workflow.compile(checkpointer=memory)
