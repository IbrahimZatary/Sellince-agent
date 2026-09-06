from functools import lru_cache

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .config import (
    LLM_TEMPERATURE,
    GROQ_API_KEY,
    GROQ_BASE_URL,
    GROQ_MODEL,
)


SYSTEM_PROMPT = """You are a telecom sales assistant.

Rules:
- Use only the provided product information for product claims.
- All provided prices are in Jordanian Dinars (JOD).
- Always display prices using JOD, never $, USD, or another currency.
- Never invent prices.
- Never invent discounts.
- Never change the customer's plan directly.
- Never promise features that are not provided.
- Keep the response clear, helpful, and suitable for the customer.
"""


@lru_cache(maxsize=1)
def get_llm() -> ChatOpenAI:
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. "
            "Add it to the backend .env file."
        )

    return ChatOpenAI(
        model=GROQ_MODEL,
        temperature=LLM_TEMPERATURE,
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL,
    )
def _format_dict(data: dict) -> str:
    return "\n".join(
        f"- {key}: {value}"
        for key, value in data.items()
    )


def generate_response(
    customer_context: dict,
    product_info: dict,
) -> str:
    llm = get_llm()

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),

        HumanMessage(
            content=(
                "Customer context:\n"
                f"{_format_dict(customer_context)}\n\n"
                "Product information:\n"
                f"{_format_dict(product_info)}\n\n"
                "Generate a customer-facing sales response using only "
                "the product information above."
            )
        ),
    ]

    response = llm.invoke(messages)

    return str(response.content)



def generate_stage_response(
    stage: str,
    customer_context: dict,
    product_info: dict,
    customer_message: str,
) -> str:
    llm = get_llm()

    messages = [
        SystemMessage(
            content=f"""
You are a telecom sales assistant.

Current conversation stage: {stage}

Rules:
- Use only the provided customer and product information.
- All prices are in JOD.
- Never invent prices, discounts, features, or benefits.
- Never claim that a plan has already been activated.
- Respond according to the current conversation stage.

Stage behavior:
- EXPLAIN_OFFER: explain the retrieved product clearly.
- HANDLE_OBJECTION: address the customer's concern without inventing discounts or features.
- CLOSE_DEAL: confirm the customer's interest and prepare them for the next step.
- ROUTE_TO_PAYMENT: tell the customer they can continue to the payment step.
"""
        ),
        HumanMessage(
            content=(
                f"Customer message:\n{customer_message}\n\n"
                f"Customer context:\n{_format_dict(customer_context)}\n\n"
                f"Product information:\n{_format_dict(product_info)}"
            )
        ),
    ]

    response = llm.invoke(messages)

    return str(response.content)