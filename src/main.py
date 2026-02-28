from src.agents.orchestrator import create_adk_brain
from src.utils.gdpr import mask_pii

def main():
    """
    Main entry point for the Omni-Resolve-Agentic system using the ADK Brain.
    """
    # Initialize the ADK Brain (Core Orchestrator)
    brain = create_adk_brain()
    
    # Initialize the system message
    print("Omni-Resolve-Agentic initialized. ADK Brain is active.")
    
    # Simulate multiple customer inquiries
    test_queries = [
        "I need help with my billing dispute for account CUST-002 (john.doe@example.com).",
        "My internet is very slow in ZIP 90210, can you check for outages?"
    ]
    
    for query in test_queries:
        # Step 1: GDPR PII Masking
        safe_query = mask_pii(query)
        print(f"\n[Incoming Inquiry]: {safe_query}")
        
        # Step 2: ADK Brain Orchestration
        # In a real environment, this would call brain.run() to process the request
        response = brain.run(safe_query)
        print(f"[Brain Response]: {response}")

if __name__ == "__main__":
    main()
