import os
import pandas as pd
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("OmniResolve-Tools")

# Load the dataset for Knowledge Base searches
DATA_PATH = os.path.join(os.getcwd(), "data", "telco_intents.csv")
try:
    kb_df = pd.read_csv(DATA_PATH)
except Exception:
    kb_df = None

@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """
    Searches the telecom knowledge base for resolutions to common customer issues.
    """
    if kb_df is None:
        return "Knowledge Base is currently unavailable."
    
    # Simple keyword-based search for prototyping
    results = kb_df[kb_df['instruction'].str.contains(query, case=False, na=False)]
    if results.empty:
        return f"No direct matches found for '{query}' in the Knowledge Base."
    
    # Return the first match's response
    match = results.iloc[0]
    return f"Resolution for '{match['intent']}':\n{match['response']}"

@mcp.tool()
def get_billing_details(customer_id: str) -> str:
    """
    Retrieves the current balance and payment status for a customer.
    """
    # Mock database for demonstration
    mock_billing = {
        "CUST-001": {"balance": "$75.50", "status": "Paid", "due_date": "2026-03-15"},
        "CUST-002": {"balance": "$120.00", "status": "Overdue", "due_date": "2026-02-15"},
    }
    details = mock_billing.get(customer_id, {"balance": "Unknown", "status": "Not Found"})
    return f"Billing Details for {customer_id}: Balance: {details['balance']}, Status: {details['status']}."

@mcp.tool()
def check_network_outage(zip_code: str) -> str:
    """
    Checks for reported network outages in a specific zip code.
    """
    # Mock outage data
    outages = ["90210", "10001"]
    if zip_code in outages:
        return f"ALER: There is a known service disruption in ZIP {zip_code}. Estimated resolution: 4 hours."
    return f"No reported outages in ZIP {zip_code}. Service is operating normally."

if __name__ == "__main__":
    mcp.run()
