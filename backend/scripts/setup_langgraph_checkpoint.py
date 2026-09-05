from app.agent.checkpoint import get_checkpointer


def main() -> None:
    with get_checkpointer() as checkpointer:
        checkpointer.setup()

    print("LangGraph checkpoint tables created successfully.")


if __name__ == "__main__":
    main()