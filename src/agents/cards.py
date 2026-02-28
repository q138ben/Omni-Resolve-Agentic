from typing import List, Optional
from pydantic import BaseModel, Field

class AgentCard(BaseModel):
    """
    The 'Diplomat' - A standardized Agent Card for A2A communication and discovery.
    """
    agent_id: str = Field(..., description="Unique identifier for the agent")
    name: str = Field(..., description="Display name of the agent")
    domain: str = Field(..., description="The primary functional domain (e.g., Billing, Tech Support)")
    description: str = Field(..., description="Detailed description of what the agent can handle")
    capabilities: List[str] = Field(default_factory=list, description="List of high-level tasks the agent performs")
    supported_intents: List[str] = Field(default_factory=list, description="Specific intents this agent is expert in")
    mcp_tools: List[str] = Field(default_factory=list, description="List of MCP tool names this agent can use")

# Define cards for the Omni-Resolve-Agentic system

ROUTER_CARD = AgentCard(
    agent_id="omni-router",
    name="OmniRouter",
    domain="Orchestration",
    description="The primary entry point that classifies and routes requests to specialized agents.",
    capabilities=["intent_classification", "agent_discovery", "request_routing"],
    supported_intents=["*"], # Handles all initial incoming requests
    mcp_tools=[]
)

BILLING_CARD = AgentCard(
    agent_id="billing-expert",
    name="BillingExpert",
    domain="Finance",
    description="Handles all inquiries related to invoices, payments, balances, and disputes.",
    capabilities=["balance_inquiry", "dispute_resolution", "payment_status"],
    supported_intents=["dispute_invoice", "invoices", "get_compensation"],
    mcp_tools=["get_billing_details"]
)

TECH_SUPPORT_CARD = AgentCard(
    agent_id="tech-support-expert",
    name="TechSupportExpert",
    domain="Technical Support",
    description="Resolves issues related to network connectivity, signal coverage, and hardware.",
    capabilities=["troubleshooting", "signal_diagnostic", "outage_checking"],
    supported_intents=["report_poor_signal_coverage", "report_problem", "network_connectivity"],
    mcp_tools=["check_network_outage", "search_knowledge_base"]
)
