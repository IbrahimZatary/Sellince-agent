import json
import re

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
  "I want the offer", "I'll take it", "I want this plan", "sounds good, I accept", "يلا اعتمد", "بدي اياه", "تم".
- ready_to_pay: the customer explicitly mentions payment, checkout, paying, or proceeding to payment.
- other: none of the above.

Bilingual & Dialect Rules:
- Support English, Modern Standard Arabic (MSA), Jordanian/Levantine Arabic slang, and Arabizi / Franco-Arab (e.g. "bdi ashtrek", "tam", "yalla").
- Jordanian/Levantine agreement terms like "يلا", "اعتمد", "بدي اياه", "توكل على الله", "سجلني", "تم" classify as accepts_offer.
- Arabic hesitations/inquiries like "لحظة", "استنى", "تفاصيل", "اشرحلي" classify as wants_details or objection accordingly.
- Arabic negations like "لا", "بديش", "ما بدي", "مش مهتم", "بطلت" classify as objection.

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


def _matches_any(text: str, words_set: set[str], patterns: list[str]) -> bool:
    for p in patterns:
        if " " in p:
            if p in text:
                return True
        else:
            if p in words_set:
                return True
    return False


def _keyword_classify(message: str) -> dict:
    msg_lower = message.lower().strip()
    words_set = set(re.findall(r"[\w']+", msg_lower))

    # 1. Price objections take highest priority (e.g. "too expensive, can't pay")
    price_concerns = [
        "expensive", "too much", "pricing", "can't afford", "cant afford", "budget", "costly",
        "غالي", "كثير غالي", "سعره مرتفع", "مكلف", "السعر عالي", "ما بقدر", "مش قادر",
    ]
    if _matches_any(msg_lower, words_set, price_concerns):
        return {"intent": "objection", "objection_type": "price"}

    # 2. General objections / negations / hesitations
    negation_patterns = [
        "no thanks", "not interested", "maybe later", "not sure", "don't want", "dont want",
        "i'm good", "im good", "changed my mind", "hesitate", "nevermind", "nvm", "stop", "cancel",
        "wait", "hold on",
        "لا", "بديش", "ما بدي", "الغاء", "بطلت", "مش مهتم", "فكنا", "انسى", "مش عاجبني",
        "لحظة", "استنى", "مش متأكد",
    ]
    if _matches_any(msg_lower, words_set, negation_patterns):
        return {"intent": "objection", "objection_type": "features"}

    # 3. Ready to pay
    pay_terms = [
        "pay", "payment", "checkout", "installment", "installments", "bank transfer", "paid",
        "route to checkout", "proceed to pay", "route me",
        "دفع", "ادفع", "رابط الدفع", "ابعثلي الرابط", "بدي ادفع",
    ]
    if _matches_any(msg_lower, words_set, pay_terms):
        return {"intent": "ready_to_pay", "objection_type": "none"}

    # 4. Accepts offer (Jordanian slang, Arabizi, English)
    accept_terms = [
        "i'll take", "i will take", "take it", "i want the offer", "i want this plan",
        "want the offer", "sign me up", "sounds good", "i accept", "accept the offer",
        "let's do it", "lets do it", "go ahead", "i want it", "i want", "okay i want",
        "ok i want", "deal", "buy", "buy it", "purchase", "ashtrek",
        "تم", "يلا", "موافق", "اشترك", "بدي اياه", "توكل على الله", "اعتمد", "خلص تم",
        "سجلني", "بدي اشترك", "موافق على العرض", "تمام اعتمد",
    ]
    if _matches_any(msg_lower, words_set, accept_terms):
        return {"intent": "accepts_offer", "objection_type": "none"}

    # 5. Wants details / questions
    detail_terms = [
        "more data", "details", "tell me", "explain", "features", "how much", "is it faster",
        "speed", "slow", "offer", "plan details", "difference", "compare", "more info",
        "does the plan", "what are my options", "upgrade", "why", "how",
        "تفاصيل", "اشرحلي اكثر", "اشرحلي", "شو التفاصيل", "كم السعر", "ايش العرض", "بدي تفاصيل", "معلومات",
        "ليش", "كيف", "شو في عروض",
    ]
    if _matches_any(msg_lower, words_set, detail_terms) or "?" in message or "؟" in message:
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
            intent = json.loads(str(response.content))
            
            # Override LLM misclassification: upgrade requests should be wants_details, not accepts_offer
            msg_lower = message.lower()
            if (intent.get("intent") == "accepts_offer" and 
                any(w in msg_lower for w in ["upgrade", "more data", "plan upgrade", "change plan"])):
                intent = {"intent": "wants_details", "objection_type": "none"}
            
            state["intent"] = intent
            state["conversation_stage"] = determine_conversation_stage(intent)
            return state
        except Exception as exc:
            print(f"[Understand] LLM classify failed, falling back to heuristics: {exc}")

    intent = _keyword_classify(message)
    state["intent"] = intent
    state["conversation_stage"] = determine_conversation_stage(intent)
    return state