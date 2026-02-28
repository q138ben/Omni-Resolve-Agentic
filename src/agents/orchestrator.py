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
        
        # Initialize the Root/Brain Agent with sub-agents
        self.brain = Agent(
            name=ROUTER_CARD.name,
            model="gemini-1.5-flash",
            instruction=(
                "You are the ADKBrain, the central orchestrator for telecom customer service. "
                "Your role is to understand the customer's intent and delegate to the appropriate expert: "
                f"- For billing, invoices, or disputes, use {BILLING_CARD.name}. "
                f"- For technical support, network, or signal issues, use {TECH_SUPPORT_CARD.name}. "
                "Maintain a high-level view of the conversation and ensure a seamless handoff."
                "Do NOT attempt to solve specialized problems yourself; always delegate to a sub-agent."
                "If the customer provides a Customer ID, ensure the Billing agent gets it."
                "If the customer provides a ZIP Code, ensure the Tech Support agent gets it."
            ),
            # Register the specialized sub-agents
            agents=[self.billing_agent, self.tech_support_agent]
        )
        
    def run(self, user_query: str) -> str:
        """
        Executes the multi-agent orchestration flow for a given query.
        """
        # Triggers the Google ADK multi-agent orchestration engine
        print(f"[Brain] Routing Inquiry: {user_query}")
        
        try:
            # Execute the orchestrator
            # This returns the result from the selected sub-agent
            result = self.brain.run(user_query)
            
            # ADK result objects typically have a 'text' or 'content' attribute
            # We convert it to a string for the UI
            if hasattr(result, 'text'):
                return result.text
            return str(result)
        except Exception as e:
            return f"I encountered an error while coordinating your request: {str(e)}"

def create_adk_brain():
    return ADKBrain()
