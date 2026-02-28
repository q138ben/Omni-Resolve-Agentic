from google.adk.agents import LlmAgent
from src.agents.cards import BILLING_CARD
from src.tools.mcp_server import get_billing_details

def create_billing_agent():
    """
    Creates a specialized Billing Agent using the BILLING_CARD metadata.
    Handles invoices, payments, and disputes using the get_billing_details MCP tool.
    """
    billing_agent = LlmAgent(
        name=BILLING_CARD.name,
        model="gemini-2.0-flash",
        instruction=(
            f"You are the {BILLING_CARD.name}, a specialist in the {BILLING_CARD.domain} domain. "
            f"Your description: {BILLING_CARD.description} "
            f"Your capabilities include: {', '.join(BILLING_CARD.capabilities)}. "
            "Use the 'get_billing_details' tool when a customer provides their ID (e.g., CUST-001). "
            "Be professional, empathetic, and clear about billing cycles and dispute processes."
        ),
        tools=[get_billing_details]
    )
    return billing_agent
