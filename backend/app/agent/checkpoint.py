from langgraph.checkpoint.postgres import PostgresSaver

from app.core.config import settings


def get_checkpointer() -> PostgresSaver:
    return PostgresSaver.from_conn_string(
        settings.DATABASE_URL
    )


def init_checkpointer_schema() -> None:
    with get_checkpointer() as checkpointer:
        checkpointer.setup()