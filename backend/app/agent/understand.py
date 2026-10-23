import json
import os
import re

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

VALID_OBJECTION_TYPES = {"price", "features", "need", "none"}


# ---------------------------------------------------------------------------
# Feature flag
# ---------------------------------------------------------------------------

def _llm_enabled() -> bool:
    """Groq is OFF by default. Set USE_LLM_UNDERSTAND=true to turn it on.

    Read at call time so the flag can be flipped without re-importing.
    """
    value = os.getenv("USE_LLM_UNDERSTAND", "false")
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_client():
    global _GROQ_CLIENT

    if _GROQ_CLIENT is None and Groq:
        api_key = os.getenv("GROQ_API_KEY")

        if api_key:
            _GROQ_CLIENT = Groq(api_key=api_key)

    return _GROQ_CLIENT


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _as_list(value):
    if not isinstance(value, list):
        return []

    return [
        item for item in value
        if isinstance(item, str)
    ]


def _normalize(message: str) -> str:
    """Lowercase and unify curly apostrophes (common on mobile keyboards)."""
    return (
        (message or "")
        .lower()
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .strip()
    )


def _has_any(text: str, phrases) -> bool:
    """Whole-word / whole-phrase match, so 'how' does not match 'show'
    and 'yes' does not match 'yesterday'."""
    return any(
        re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text)
        for phrase in phrases
    )


# ---------------------------------------------------------------------------
# Keyword classifier (primary path, no external AI needed)
# ---------------------------------------------------------------------------

PAYMENT_WORDS = (
    "pay", "payment", "checkout", "installment", "installments",
    "bank transfer", "paid",
)

ACCEPT_PHRASES = (
    "i'll take", "i will take", "take it", "i want the offer",
    "i want this plan", "want the offer", "sign me up", "sounds good",
    "i accept", "accept the offer", "let's do it", "lets do it",
    "go ahead", "i want it",
)

PRICE_OBJECTION_PHRASES = (
    "expensive", "too much", "pricing", "can't afford", "cant afford",
    "budget",
)

OTHER_OBJECTION_PHRASES = (
    "no thanks", "not interested", "maybe later", "not sure",
    "don't want", "dont want", "i'm good", "im good", "changed my mind",
    "hesitate", "hold on", "wait",
)

DETAIL_PHRASES = (
    "more data", "details", "tell me", "explain", "features", "how much",
    "is it faster", "speed", "slow", "offer", "plan details", "difference",
    "compare", "more info", "does the plan", "what are my options",
    "upgrade",
)

QUESTION_WORDS = (
    "how", "what", "when", "where", "why", "can i", "is there",
)


def _keyword_classify(message: str) -> dict:
    text = _normalize(message)

    intent = "other"
    objection_type = "none"

    if _has_any(text, PAYMENT_WORDS):
        intent = "ready_to_pay"

    elif _has_any(text, ACCEPT_PHRASES):
        intent = "accepts_offer"

    elif _has_any(text, PRICE_OBJECTION_PHRASES + OTHER_OBJECTION_PHRASES):
        intent = "objection"
        objection_type = (
            "price"
            if _has_any(text, PRICE_OBJECTION_PHRASES)
            else "features"
        )

    elif _has_any(text, DETAIL_PHRASES):
        intent = "wants_details"

    # needs / questions / objections (used by recommend_node via
    # intent["needs"]).
    needs = []
    questions = []
    objections = []

    if any(w in text for w in (
        "upgrade", "more data", "change my plan", "need data",
        "slow", "run out", "gb",
    )):
        needs.append("plan upgrade")

    if any(w in text for w in (
        "bill", "price", "cost", "cheaper", "expensive",
    )):
        needs.append("billing inquiry")

    if any(w in text for w in (
        "renew", "contract", "expire", "end date",
    )):
        needs.append("contract renewal")

    if "?" in message or _has_any(text, QUESTION_WORDS):
        questions.append(message.strip())

    if intent == "objection" or _has_any(text, (
        "too expensive", "expensive", "not interested",
        "dont want", "don't want", "no thanks",
    )):
        objections.append("price or interest concern")

    return {
        "intent": intent,
        "objection_type": objection_type,
        "needs": needs,
        "questions": questions,
        "objections": objections,
    }


# ---------------------------------------------------------------------------
# Explicit purchase / payment detection (rule-based, always runs)
# ---------------------------------------------------------------------------

def _detect_purchase_intent(message: str, previous_stage: str | None) -> str | None:
    text = _normalize(message)

    payment_phrases = (
        "complete the purchase",
        "complete my purchase",
        "proceed to checkout",
        "go to checkout",
        "ready to pay",
        "make the payment",
        "pay now",
        "checkout",
    )

    purchase_phrases = (
        "i want to purchase",
        "i want to buy",
        "i'd like to buy",
        "i would like to buy",
        "purchase this upgrade",
        "buy this upgrade",
    )

    if _has_any(text, payment_phrases):
        return "ready_to_pay"

    if _has_any(text, purchase_phrases):
        return "ready_to_pay"

    if previous_stage == "CLOSE_DEAL" and _has_any(text, (
        "yes",
        "i confirm",
        "i agree",
        "confirmed",
    )):
        return "ready_to_pay"

    return None


# ---------------------------------------------------------------------------
# Optional Groq extraction (disabled unless USE_LLM_UNDERSTAND=true)
# ---------------------------------------------------------------------------

def _llm_extract(state: AgentState, message: str, previous_stage: str | None):
    client = _get_client()

    if not client:
        return None

    try:
        prompt = f"""
Analyze this telecom customer message and extract its intent.

Customer message:
{json.dumps(message, ensure_ascii=False)}

Conversation context:
Current offer:
{json.dumps(state.get("active_offer") or state.get("offer"), ensure_ascii=False, default=str)}

Previous conversation stage:
{previous_stage}

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

        parsed = json.loads(completion.choices[0].message.content or "{}")

        if not isinstance(parsed, dict):
            return None

        # Upgrade requests are details requests, not acceptance.
        text = _normalize(message)
        if parsed.get("intent") == "accepts_offer" and _has_any(text, (
            "upgrade", "more data", "plan upgrade", "change plan",
        )):
            parsed["intent"] = "wants_details"
            parsed["objection_type"] = "none"

        return parsed

    except Exception as exc:
        print(f"[Groq Understand] Falling back to keywords: {exc}")
        return None


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

def understand_node(state: AgentState) -> AgentState:
    """
    Stage 2: UNDERSTAND

    Primary path: deterministic keyword classifier (no external AI).
    Optional path: Groq extraction when USE_LLM_UNDERSTAND=true; falls
    back to the keyword classifier if Groq is unavailable or fails.

    Explicit purchase/payment intent is always rule-based and takes
    priority. The conversation stage is recomputed on EVERY message, so a
    message that maps to no stage (intent "other") clears the previous
    stage instead of leaving it stuck in the checkpoint.
    """

    message = state.get("message") or ""

    # Read BEFORE the stage is overwritten below; the "yes" confirmation
    # after CLOSE_DEAL depends on it.
    previous_stage = state.get("conversation_stage")

    parsed = None

    if _llm_enabled():
        parsed = _llm_extract(state, message, previous_stage)

    if parsed is None:
        parsed = _keyword_classify(message)

    intent_type = parsed.get("intent", "other")

    if intent_type not in VALID_INTENTS:
        intent_type = "other"

    objection_type = parsed.get("objection_type", "none")

    if objection_type not in VALID_OBJECTION_TYPES:
        objection_type = "none"

    intent_data = {
        "intent": intent_type,
        "objection_type": objection_type,
        "needs": _as_list(parsed.get("needs")),
        "questions": _as_list(parsed.get("questions")),
        "objections": _as_list(parsed.get("objections")),
    }

    detected_intent = _detect_purchase_intent(message, previous_stage)

    if detected_intent:
        intent_data["intent"] = detected_intent
        intent_data["needs"] = list(
            dict.fromkeys(intent_data["needs"] + ["purchase"])
        )

    state["intent"] = intent_data

    # Always overwrite: None for intents with no stage (e.g. "other")
    # so the previous stage cannot leak into this turn.
    state["conversation_stage"] = determine_conversation_stage(intent_data)

    return state