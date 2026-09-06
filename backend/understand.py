import json
import os
from agent_state import AgentState

try:
    from groq import Groq
except ImportError:
    Groq = None


def understand_node(state: AgentState) -> AgentState:
    """Stage 2: UNDERSTAND Node powered by Groq.
    Extracts structured intent (needs, questions, objections) from user message.
    """
    message = state.get("message") or ""
    api_key = os.getenv("GROQ_API_KEY")

    if Groq and api_key:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""
Analyze this telecom customer message and extract their intent into a JSON object:
Message: "{message}"

Return ONLY a JSON object with this exact structure:
{{
    "needs": ["list of detected needs like 'plan upgrade', 'more data', 'bill inquiry'"],
    "questions": ["any direct or indirect questions asked"],
    "objections": ["any complaints, hesitations, or pricing concerns"]
}}
"""
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a customer intent extraction engine. Respond strictly with JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
                response_format={"type": "json_object"},
            )
            parsed = json.loads(completion.choices[0].message.content)
            state["intent"] = {
                "needs": parsed.get("needs", []),
                "questions": parsed.get("questions", []),
                "objections": parsed.get("objections", []),
            }
            return state
        except Exception as e:
            print(f"[Groq Understand] Falling back to heuristics: {e}")

    # Deterministic fallback if offline or no key
    msg_lower = message.lower()
    needs, questions, objections = [], [], []

    if any(w in msg_lower for w in ["upgrade", "more data", "change my plan", "need data", "slow", "run out", "gb"]):
        needs.append("plan upgrade")
    if any(w in msg_lower for w in ["bill", "price", "cost", "cheaper", "expensive"]):
        needs.append("billing inquiry")
    if any(w in msg_lower for w in ["renew", "contract", "expire", "end date"]):
        needs.append("contract renewal")

    if "?" in message or any(w in msg_lower for w in ["how", "what", "when", "where", "why", "can i", "is there"]):
        questions.append(message.strip())

    if any(w in msg_lower for w in ["too expensive", "expensive", "not interested", "dont want", "don't want", "no thanks"]):
        objections.append("price or interest concern")

    state["intent"] = {
        "needs": needs,
        "questions": questions,
        "objections": objections,
    }
    return state
