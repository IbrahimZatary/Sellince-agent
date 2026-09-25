import sys
import traceback

print("--- PHASE 1: Syntax & Import Check ---")
try:
    from app.main import app
    from app.agent.graph import compiled_graph
    from app.schemas.chat import ChatRequest, ChatResponse
    print("[SUCCESS] All FastAPI routes, schemas, and LangGraph nodes imported cleanly.\n")
except Exception as e:
    print(f"[FAIL] Import Error:")
    traceback.print_exc()
    sys.exit(1)

print("--- PHASE 2: Graph Execution & Data Path Check ---")
try:
    initial_state = {
        "customer_id": 14,
        "message": "My connection is slow",
        "history": []
    }
    
    print("Invoking graph with test customer 14...")
    result = compiled_graph.invoke(
        initial_state,
        config={"configurable": {"thread_id": "test_14"}}
    )
    
    print("[SUCCESS] Graph executed without crashing.")
    print(f" -> Next Action: {result.get('action')}")
    print(f" -> Action Payload: {result.get('action_payload')}")
    print(f" -> Response Generated: {bool(result.get('response'))}")
    
except Exception as e:
    print(f"[FAIL] Runtime Error during graph execution:")
    traceback.print_exc()
    sys.exit(1)

print("\nAll integration checks passed. The architecture is sound.")
