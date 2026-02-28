import os
import vertexai
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from src.agents.cards import ROUTER_CARD, BILLING_CARD, TECH_SUPPORT_CARD
from src.agents.billing import create_billing_agent
from src.agents.tech_support import create_tech_support_agent
import asyncio

# Recommended stable model name for Vertex AI in 2026
MODEL_NAME = "gemini-2.0-flash"

class ADKBrain:
    """
    The Core Orchestrator (The Brain) of the Omni-Resolve-Agentic system.
    Uses Google ADK Runner to manage sessions and delegate to specialized sub-agents.
    """
    def __init__(self):
        # Initialize Vertex AI with the project and location from environment
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        if project:
            print(f"[Brain] Initializing Vertex AI: project={project}, location={location}")
            vertexai.init(project=project, location=location)
        
        # Initialize sub-agents
        self.billing_agent = create_billing_agent()
        self.tech_support_agent = create_tech_support_agent()
        
        # Initialize the Root/Brain Agent
        self.brain = LlmAgent(
            name=ROUTER_CARD.agent_id,
            model=MODEL_NAME,
            instruction=(
                "You are the ADKBrain, the central orchestrator for telecom customer service. "
                "Your role is to understand the customer's intent and delegate to the appropriate expert: "
                f"- For billing, invoices, or disputes, transfer to {BILLING_CARD.name}. "
                f"- For technical support, network, or signal issues, transfer to {TECH_SUPPORT_CARD.name}. "
                "Maintain a high-level view of the conversation and ensure a seamless handoff."
                "Do NOT attempt to solve specialized problems yourself; always delegate."
            ),
            sub_agents=[self.billing_agent, self.tech_support_agent]
        )
        
        # Initialize the Session Service
        self.session_service = InMemorySessionService()
        
        # Initialize the Runner with the session service
        self.runner = Runner(
            agent=self.brain,
            app_name="OmniResolveAgentic",
            session_service=self.session_service,
            auto_create_session=True
        )
        
    async def run(self, user_query: str) -> str:
        """
        Executes the multi-agent orchestration flow via the Runner.
        """
        print(f"[Brain] Routing Inquiry: {user_query}")
        
        # Wrap the query in a Content object
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=user_query)]
        )
        
        full_response = ""
        try:
            # Runner handles InvocationContext and Session internally
            async for event in self.runner.run_async(
                user_id="default_user",
                session_id="default_session",
                new_message=new_message
            ):
                # Handle the final response
                if hasattr(event, 'is_final_response') and event.is_final_response():
                    if hasattr(event, 'content') and event.content:
                        if hasattr(event.content, 'parts'):
                            text_parts = [p.text for p in event.content.parts if hasattr(p, 'text') and p.text]
                            if text_parts:
                                return "".join(text_parts)
                        return str(event.content)
                
                # Accumulate partial responses
                if hasattr(event, 'partial') and event.partial:
                    if hasattr(event, 'content') and event.content:
                        if hasattr(event.content, 'parts'):
                            for part in event.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    full_response += part.text
            
            return full_response if full_response else "No response received from the agent."
            
        except Exception as e:
            print(f"[Brain Error] {str(e)}")
            return f"I encountered an error while coordinating your request: {str(e)}"

def create_adk_brain():
    return ADKBrain()
