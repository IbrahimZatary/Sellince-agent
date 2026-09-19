import json

from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.agent_state import AgentState
from app.agent.conversation import determine_conversation_stage
from app.rag.response_generator import get_llm


SYSTEM_PROMPT = """
You classify customer messages for a telecom sales conversation.

Return ONLY valid JSON in this exact format:
{
  "intent": "wants_details | objection | accepts_offer | ready_to_pay | other",
  "objection_type": "price | features | need | none"
}

Rules:
- wants_details: the customer asks a question or requests more information about the offer.
- objection: the customer expresses concern, hesitation, rejection, or dissatisfaction.
- accepts_offer: the customer clearly agrees to take or accept the offer, for example:
  "I want the offer", "I'll take it", "I want this plan", "sounds good, I accept".
- ready_to_pay: the customer explicitly mentions payment, checkout, paying, or proceeding to payment.
- other: none of the above.

Important:
- Agreement to take the offer is accepts_offer, NOT wants_details.
- Only classify as wants_details when the customer is actually asking for information.
- If the customer explicitly mentions payment, ready_to_pay takes priority over accepts_offer.

Do not include explanations outside the JSON.
"""

_LLM = None


def _get_llm():
    global _LLM
    if _LLM is None:
        try:
            _LLM = get_llm()
        except RuntimeError:
            _LLM = None
    return _LLM


def _parse_intent(payload: str) -> dict:
    text = payload.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    data = json.loads(text)
    data["intent"] = data.get("intent") or "other"
    if data["intent"] not in (
        "wants_details",
        "objection",
        "accepts_offer",
        "ready_to_pay",
        "other",
    ):
        data["intent"] = "other"
    data["objection_type"] = data.get("objection_type") or "none"
    return data


def _keyword_classify(message: str) -> dict:
    msg_lower = message.lower()

    if any(w in msg_lower for w in [
        "pay", "payment", "checkout", "installment", "installments", "bank transfer", "paid",
    ]):
        return {"intent": "ready_to_pay", "objection_type": "none"}

    if any(w in msg_lower for w in [
        "i'll take", "i will take", "take it", "i want the offer", "i want this plan",
        "want the offer", "sign me up", "sounds good", "i accept", "accept the offer",
        "let's do it", "lets do it", "go ahead",
    ]):
        return {"intent": "accepts_offer", "objection_type": "none"}

    price_concerns = ["expensive", "too much", "pricing", "can't afford", "cant afford", "budget"]
    if any(w in msg_lower for w in price_concerns + [
        "no thanks", "not interested", "maybe later", "not sure", "don't want", "dont want",
        "i'm good", "im good", "changed my mind", "hesitate", "hold on", "wait",
    ]):
        objection_type = "price" if any(w in msg_lower for w in price_concerns) else "features"
        return {"intent": "objection", "objection_type": objection_type}

    if any(w in msg_lower for w in [
        "more data", "details", "tell me", "explain", "features", "how much", "is it faster",
        "speed", "slow", "offer", "plan details", "difference", "compare", "more info",
        "does the plan", "what are my options",
    ]):
        return {"intent": "wants_details", "objection_type": "none"}

    return {"intent": "other", "objection_type": "none"}


def understand_node(state: AgentState) -> AgentState:
    """Stage 2: UNDERSTAND Node powered by Groq.

    Classifies the customer message into an intent (wants_details / objection /
    accepts_offer / ready_to_pay / other) and maps it to a conversation stage.
    Falls back to deterministic keyword classification when Groq is unavailable.
    """
    message = state.get("message") or ""
    llm = _get_llm()

    if llm:
        try:
            response = llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=message),
            ])
            intent = _parse_intent(str(response.content))
            state["intent"] = intent
            state["conversation_stage"] = determine_conversation_stage(intent)
            return state
        except Exception as exc:
            print(f"[Understand] LLM classify failed, falling back to heuristics: {exc}")

    intent = _keyword_classify(message)
    state["intent"] = intent
    state["conversation_stage"] = determine_conversation_stage(intent)
    return state