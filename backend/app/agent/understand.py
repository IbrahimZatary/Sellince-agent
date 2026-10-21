
import json
import os

from dotenv import load_dotenv

from app.agent.agent_state import AgentState
from app.agent.conversation import determine_conversation_stage

try:
    from groq import Groq
except ImportError:
    Groq = None


load_dotenv()

_GROQ_CLIENT = None

MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

VALID_INTENTS = {
    "wants_details",
    "objection",
    "accepts_offer",
    "ready_to_pay",
    "other",
}


def _get_client():
    global _GROQ_CLIENT

    if _GROQ_CLIENT is None and Groq:
        api_key = os.getenv("GROQ_API_KEY")

        if api_key:
            _GROQ_CLIENT = Groq(api_key=api_key)

    return _GROQ_CLIENT


def _as_list(value):
    if not isinstance(value, list):
        return []

    return [
        item for item in value
        if isinstance(item, str)
    ]


def understand_node(state: AgentState) -> AgentState:
    """
    Stage 2: UNDERSTAND

    Uses Kareem's Groq-based extraction of needs,
    questions and objections.

    Adds the original sales intent and conversation
    stage required by the existing agent workflow.
    """

    message = state.get("message") or ""
    client = _get_client()

    parsed = None

    if client:
        try:
            prompt = f"""
Analyze this telecom customer message and extract its intent.

Customer message:
{json.dumps(message, ensure_ascii=False)}

Conversation context:
Current offer:
{json.dumps(state.get("active_offer") or state.get("offer"), ensure_ascii=False, default=str)}

Previous conversation stage:
{state.get("conversation_stage")}

Return ONLY a valid JSON object with this exact structure:
{{
    "intent": "wants_details | objection | accepts_offer | ready_to_pay | other",
    "objection_type": "price | features | need | none",
    "needs": [],
    "questions": [],
    "objections": []
}}

Intent classification:
- wants_details: customer asks for details about an offer.
- objection: customer expresses hesitation or concern about an offer.
- accepts_offer: customer explicitly accepts an offer.
- ready_to_pay: customer explicitly requests checkout or payment.
- other: none of the above.

Rules:
- Explicit payment or checkout intent takes priority over acceptance.
- Do not classify a casual agreement as acceptance without context.
- Do not interpret a technical complaint as an automatic purchase request.
- Keep needs, questions, and objections as lists of strings.
- Do not invent customer information or product offers.
"""

            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a telecom customer intent extraction "
                            "engine. Return strictly valid JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.0,
                response_format={"type": "json_object"},
            )

            parsed = json.loads(
                completion.choices[0].message.content or "{}"
            )

            if not isinstance(parsed, dict):
                parsed = None

        except Exception as exc:
            print(
                f"[Groq Understand] "
                f"Falling back to heuristics: {exc}"
            )

    # Preserve Kareem's deterministic fallback
    # when Groq is unavailable.
    if parsed is None:
        msg_lower = message.lower()

        needs = []
        questions = []
        objections = []

        if any(w in msg_lower for w in [
            "upgrade",
            "more data",
            "change my plan",
            "need data",
            "slow",
            "run out",
            "gb",
        ]):
            needs.append("plan upgrade")

        if any(w in msg_lower for w in [
            "bill",
            "price",
            "cost",
            "cheaper",
            "expensive",
        ]):
            needs.append("billing inquiry")

        if any(w in msg_lower for w in [
            "renew",
            "contract",
            "expire",
            "end date",
        ]):
            needs.append("contract renewal")

        if "?" in message or any(w in msg_lower for w in [
            "how",
            "what",
            "when",
            "where",
            "why",
            "can i",
            "is there",
        ]):
            questions.append(message.strip())

        if any(w in msg_lower for w in [
            "too expensive",
            "expensive",
            "not interested",
            "dont want",
            "don't want",
            "no thanks",
        ]):
            objections.append("price or interest concern")

        # The original fallback does not classify
        # sales acceptance or payment.
        parsed = {
            "intent": "other",
            "objection_type": "none",
            "needs": needs,
            "questions": questions,
            "objections": objections,
        }

    intent_type = parsed.get("intent", "other")

    if intent_type not in VALID_INTENTS:
        intent_type = "other"

    objection_type = parsed.get("objection_type", "none")

    if objection_type not in {
        "price",
        "features",
        "need",
        "none",
    }:
        objection_type = "none"

    intent_data = {
        "intent": intent_type,
        "objection_type": objection_type,
        "needs": _as_list(parsed.get("needs")),
        "questions": _as_list(parsed.get("questions")),
        "objections": _as_list(parsed.get("objections")),
    }

    state["intent"] = intent_data

    # Use the existing conversation-stage mapping.
    stage = determine_conversation_stage(intent_data)

    if stage is not None:
        state["conversation_stage"] = stage

    return state
