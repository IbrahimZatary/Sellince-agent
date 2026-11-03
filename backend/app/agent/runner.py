
from app.agent.checkpoint import get_checkpointer
from app.agent.graph import build_graph


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


def run_proactive_session(
    conversation_id: int,
    customer_id: int,
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
            {
                "customer_id": customer_id,
                "conversation_id": conversation_id,
                "entry_type": "proactive",
            },
            config=config,
        )

    return result

def has_existing_checkpoint(conversation_id: int) -> bool:
    config = {
        "configurable": {
            "thread_id": str(conversation_id)
        }
    }

    with get_checkpointer() as checkpointer:
        checkpoint = checkpointer.get(config)

    return checkpoint is not None
