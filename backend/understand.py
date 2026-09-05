import json

from langchain_core.messages import HumanMessage, SystemMessage

from agent_state import AgentState
from app.rag.response_generator import get_llm
from conversation import determine_conversation_stage


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


def understand_node(state: AgentState) -> AgentState:
    llm = get_llm()

    message = state["message"]

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=message),
    ])

    intent = json.loads(str(response.content))

    state["intent"] = intent
    state["conversation_stage"] = determine_conversation_stage(intent)

    return state