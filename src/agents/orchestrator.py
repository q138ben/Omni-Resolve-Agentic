from google.adk.agents.llm_agent import Agent
from src.agents.cards import ROUTER_CARD, BILLING_CARD, TECH_SUPPORT_CARD
from src.agents.billing import create_billing_agent
from src.agents.tech_support import create_tech_support_agent

class ADKBrain:
    """
    The Core Orchestrator (The Brain) of the Omni-Resolve-Agentic system.
    Uses Google ADK to manage and delegate to specialized sub-agents.
    """
    def __init__(self):
        # Initialize sub-agents
        self.billing_agent = create_billing_agent()
        self.tech_support_agent = create_tech_support_agent()
        
        # Initialize the Root/Brain Agent
        self.brain = Agent(
            name=ROUTER_CARD.name,
            model="gemini-1.5-flash",
            instruction=(
                "You are the ADKBrain, the central orchestrator for telecom customer service. "
                "Your role is to understand the customer's intent and delegate to the appropriate expert: "
                f"- For billing, invoices, or disputes, use {BILLING_CARD.name}. "
                f"- For technical support, network, or signal issues, use {TECH_SUPPORT_CARD.name}. "
                "Maintain a high-level view of the conversation and ensure a seamless handoff."
                "Do NOT attempt to solve specialized problems yourself; always delegate."
            ),
            # Sub-agents: [self.billing_agent, self.tech_support_agent]
        )
        
    def run(self, user_query: str):
        """
        Executes the multi-agent orchestration flow for a given query.
        """
        # In a full ADK setup, this would use self.brain.run(user_query)
        # which would trigger the internal orchestration engine.
        print(f"[Brain] Received: {user_query}")
        return f"Brain is processing the request with Google ADK orchestrator..."

def create_adk_brain():
    return ADKBrain()
