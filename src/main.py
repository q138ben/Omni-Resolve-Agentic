import asyncio
from src.agents.orchestrator import create_adk_brain
from src.utils.gdpr import mask_pii
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def run_test():
    """
    Main test entry point for the Omni-Resolve-Agentic system using the ADK Brain.
    """
    # Initialize the ADK Brain (Core Orchestrator)
    brain = create_adk_brain()
    
    # Initialize the system message
    print("Omni-Resolve-Agentic initialized. ADK Brain is active.\n")
    
    # Simulate multiple customer inquiries
    test_queries = [
        "I have a billing dispute for account CUST-002 (john.doe@example.com).",
        "My internet is very slow in ZIP 90210, can you check for outages?"
    ]
    
    for query in test_queries:
        # Step 1: GDPR PII Masking
        safe_query = mask_pii(query)
        print(f"--- Incoming Inquiry: {safe_query} ---")
        
        # Step 2: ADK Brain Orchestration (Async)
        try:
            response = await brain.run(safe_query)
            print(f"--- Brain Response ---\n{response}\n")
        except Exception as e:
            print(f"--- Brain Error ---\n{str(e)}\n")

if __name__ == "__main__":
    asyncio.run(run_test())
