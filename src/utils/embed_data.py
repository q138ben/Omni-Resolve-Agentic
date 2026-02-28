import os
import pandas as pd
import numpy as np
from vertexai.language_models import TextEmbeddingModel
from dotenv import load_dotenv
import vertexai

load_dotenv()

def embed_knowledge_base():
    """
    Generates and saves embeddings for the knowledge base using Vertex AI.
    """
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    vertexai.init(project=project, location=location)
    
    data_path = "data/telco_intents.csv"
    dest_path = "data/telco_embeddings.npy"
    
    if not os.path.exists(data_path):
        print("Dataset not found. Run download_data.py first.")
        return

    print("Loading dataset...")
    df = pd.read_csv(data_path)
    
    # For prototype, we'll embed the first 1,000 rows (fast and effective)
    sample_size = 1000
    subset = df.head(sample_size).copy()
    
    print(f"Embedding {sample_size} rows with Vertex AI (text-embedding-004)...")
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    instructions = subset['instruction'].tolist()
    
    # Batch processing to respect API limits
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(instructions), batch_size):
        batch = instructions[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}...")
        embeddings = model.get_embeddings(batch)
        all_embeddings.extend([e.values for e in embeddings])
        
    # Save the embeddings and the subset
    np.save(dest_path, np.array(all_embeddings))
    subset.to_csv("data/telco_subset_with_embeddings.csv", index=False)
    
    print(f"Successfully saved {len(all_embeddings)} embeddings to {dest_path}")

if __name__ == "__main__":
    embed_knowledge_base()
