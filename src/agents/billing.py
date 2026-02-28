from google.adk.agents.llm_agent import Agent
from src.agents.cards import BILLING_CARD

def create_billing_agent():
    """
    Creates a specialized Billing Agent using the BILLING_CARD metadata.
    Handles invoices, payments, and disputes.
    """
    billing_agent = Agent(
        name=BILLING_CARD.name,
        model="gemini-1.5-flash",
        instruction=(
            f"You are the {BILLING_CARD.name}, a specialist in the {BILLING_CARD.domain} domain. "
            f"Your description: {BILLING_CARD.description} "
            f"Your capabilities include: {', '.join(BILLING_CARD.capabilities)}. "
            "Use the 'get_billing_details' tool when a customer provides their ID (e.g., CUST-001). "
            "Be professional, empathetic, and clear about billing cycles and dispute processes."
        ),
        # In a full ADK setup, tools would be registered here
        # tools=["get_billing_details"]
    )
    return billing_agent
