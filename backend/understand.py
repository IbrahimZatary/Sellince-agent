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

Intent rules:

- wants_details:
  The customer asks a question or requests more information
  about the offer.
  Examples:
  "Tell me more"
  "What does the plan include?"
  "Can you explain the offer?"

- objection:
  The customer expresses concern, hesitation, rejection,
  or dissatisfaction.
  Examples:
  "It is too expensive"
  "I don't need it"
  "I'm not sure about the features"

- accepts_offer:
  The customer clearly agrees to, accepts, or shows clear
  interest in proceeding with the offered product or plan.
  Examples:
  "Yes, I'm interested"
  "I am interested"
  "I want the offer"
  "I'll take it"
  "I want this plan"
  "Sounds good, I accept"
  "Yes, I want it"

- ready_to_pay:
  The customer explicitly mentions payment, checkout,
  paying, or proceeding to payment.
  Examples:
  "I am ready to pay"
  "Take me to checkout"
  "How can I pay?"
  "Proceed to payment"

- other:
  The message does not match any of the intents above.
  Examples:
  "Hi"
  "Hello"
  "Okay"

Important:
- "Yes, I'm interested" and equivalent expressions of clear
  interest in the offer are accepts_offer.
- Agreement to take or proceed with the offer is
  accepts_offer, NOT wants_details.
- Only classify as wants_details when the customer is
  actually asking for information.
- If the customer explicitly mentions payment,
  ready_to_pay takes priority over accepts_offer.
- When intent is not objection, objection_type must be
  "none".

Do not include explanations outside the JSON.
"""


def parse_intent_response(content) -> dict:
    if isinstance(content, str):
        text = content.strip()
    else:
        text = str(content).strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return json.loads(text)


def understand_node(state: AgentState) -> AgentState:
    llm = get_llm()

    message = state["message"]

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=message),
    ])

    intent = parse_intent_response(response.content)

    state["intent"] = intent

    previous_stage = state.get("conversation_stage")

    state["conversation_stage"] = determine_conversation_stage(
        intent,
        previous_stage,
    )

    return state