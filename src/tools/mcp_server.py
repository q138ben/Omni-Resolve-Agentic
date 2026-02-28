import os
import pandas as pd
import numpy as np
from mcp.server.fastmcp import FastMCP
from sklearn.metrics.pairwise import cosine_similarity
from vertexai.language_models import TextEmbeddingModel
import vertexai

# Initialize the MCP server
mcp = FastMCP("OmniResolve-Tools")

# Paths for Knowledge Base
DATA_PATH = os.path.join(os.getcwd(), "data", "telco_subset_with_embeddings.csv")
EMBED_PATH = os.path.join(os.getcwd(), "data", "telco_embeddings.npy")

# Global variables for KB data
kb_df = None
kb_embeddings = None
embedding_model = None

def load_kb():
    global kb_df, kb_embeddings, embedding_model
    try:
        if os.path.exists(DATA_PATH) and os.path.exists(EMBED_PATH):
            kb_df = pd.read_csv(DATA_PATH)
            kb_embeddings = np.load(EMBED_PATH)
            # Initialize the embedding model for real-time query embedding
            project = os.getenv("GOOGLE_CLOUD_PROJECT")
            if project:
                vertexai.init(project=project, location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"))
                embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
            print(f"Semantic Knowledge Base loaded with {len(kb_df)} entries.")
        else:
            # Fallback to full dataset if embeddings aren't ready
            full_path = os.path.join(os.getcwd(), "data", "telco_intents.csv")
            if os.path.exists(full_path):
                kb_df = pd.read_csv(full_path)
                print("Keyword Knowledge Base loaded (Semantic search unavailable).")
    except Exception as e:
        print(f"Error loading KB: {e}")

# Initial load
load_kb()

@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """
    Searches the telecom knowledge base for resolutions using Semantic Search.
    Falls back to keyword search if embeddings are unavailable.
    """
    if kb_df is None:
        return "Knowledge Base is currently unavailable."
    
    # 1. Try Semantic Search
    if kb_embeddings is not None and embedding_model is not None:
        try:
            # Embed the query
            query_embedding = embedding_model.get_embeddings([query])[0].values
            
            # Calculate cosine similarity
            similarities = cosine_similarity([query_embedding], kb_embeddings)[0]
            
            # Get the top match
            top_index = np.argmax(similarities)
            score = similarities[top_index]
            
            if score > 0.6: # Threshold for semantic relevance
                match = kb_df.iloc[top_index]
                return f"[Semantic Match - Score: {score:.2f}] Resolution for '{match['intent']}':\n{match['response']}"
        except Exception as e:
            print(f"Semantic search failed, falling back: {e}")

    # 2. Fallback to Keyword Search
    results = kb_df[kb_df['instruction'].str.contains(query, case=False, na=False)]
    if not results.empty:
        match = results.iloc[0]
        return f"[Keyword Match] Resolution for '{match['intent']}':\n{match['response']}"
    
    return f"No matches found for '{query}' in the Knowledge Base."

@mcp.tool()
def get_billing_details(customer_id: str) -> str:
    """
    Retrieves the current balance and payment status for a customer.
    """
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
    outages = ["90210", "10001"]
    if zip_code in outages:
        return f"ALERT: There is a known service disruption in ZIP {zip_code}. Estimated resolution: 4 hours."
    return f"No reported outages in ZIP {zip_code}. Service is operating normally."

if __name__ == "__main__":
    mcp.run()
