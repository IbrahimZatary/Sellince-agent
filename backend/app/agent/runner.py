from app.agent.checkpoint import get_checkpointer
from graph import build_graph


def run_agent_turn(
    conversation_id: int,
    state: dict,
) -> dict:
    config = {
        "configurable": {
            "thread_id": str(conversation_id)
        }
    }

    with get_checkpointer() as checkpointer:
        graph = build_graph().compile(
            checkpointer=checkpointer
        )

        result = graph.invoke(
            state,
            config=config,
        )

    return result