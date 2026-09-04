from app.agent.agent_state import AgentState


def understand_node(state: AgentState) -> AgentState:
    # TEMP STUB -- no Anthropic API key yet. Restore the real LLM call once available.
    # Simple keyword check so we can test intent-based branching without a real LLM.
    message = state["message"].lower()
    needs = []
    if "upgrade" in message or "more data" in message or "change my plan" in message:
        needs.append("plan upgrade")

    state["intent"] = {"needs": needs, "questions": [], "objections": []}
    return state