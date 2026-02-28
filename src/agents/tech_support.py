from google.adk.agents.llm_agent import Agent
from src.agents.cards import TECH_SUPPORT_CARD
from src.tools.mcp_server import check_network_outage, search_knowledge_base

def create_tech_support_agent():
    """
    Creates a specialized Technical Support Agent using the TECH_SUPPORT_CARD metadata.
    Handles network, signal, and troubleshooting issues using MCP tools.
    """
    tech_agent = Agent(
        name=TECH_SUPPORT_CARD.name,
        model="gemini-1.5-flash",
        instruction=(
            f"You are the {TECH_SUPPORT_CARD.name}, a specialist in the {TECH_SUPPORT_CARD.domain} domain. "
            f"Your description: {TECH_SUPPORT_CARD.description} "
            f"Your capabilities include: {', '.join(TECH_SUPPORT_CARD.capabilities)}. "
            "Use 'check_network_outage' for zip-code-related issues. "
            "Use 'search_knowledge_base' to find troubleshooting steps from the telecom dataset. "
            "Provide step-by-step guidance and maintain a helpful, technical tone."
        ),
        tools=[check_network_outage, search_knowledge_base]
    )
    return tech_agent
