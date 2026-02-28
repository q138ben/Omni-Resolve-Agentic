from src.agents.router import create_router_agent
from src.utils.gdpr import mask_pii

def main():
    """
    Main entry point for the Omni-Resolve-Agentic system.
    """
    # Initialize the router agent
    router = create_router_agent()
    
    # Placeholder for the main loop or entry for an inquiry
    print("Omni-Resolve-Agentic initialized. Starting service...")
    
    # Mocking a user input
    user_input = "Hello, I have a billing issue with my account (john.doe@example.com)."
    
    # GDPR-compliant masking
    safe_input = mask_pii(user_input)
    print(f"Masked user input: {safe_input}")
    
    # Placeholder for routing and tool execution
    # In a real scenario, this would use the ADK orchestration engine.
    print(f"OmniRouter is processing the inquiry: {safe_input}")

if __name__ == "__main__":
    main()
