import os
import pandas as pd
from huggingface_hub import hf_hub_download

def download_bitext_telco():
    """
    Downloads the Bitext Telco LLM Chatbot Training Dataset from Hugging Face.
    Repository: bitext/Bitext-telco-llm-chatbot-training-dataset
    """
    repo_id = "bitext/Bitext-telco-llm-chatbot-training-dataset"
    filename = "bitext-telco-llm-chatbot-training-dataset.csv"
    
    # Define the destination path
    data_dir = os.path.join(os.getcwd(), "data")
    dest_path = os.path.join(data_dir, "telco_intents.csv")
    
    print(f"Downloading dataset from {repo_id}...")
    
    try:
        # Download the file
        file_path = hf_hub_download(repo_id=repo_id, filename=filename, repo_type="dataset")
        
        # Load and save to the local data directory
        df = pd.read_csv(file_path)
        df.to_csv(dest_path, index=False)
        
        print(f"Dataset successfully downloaded and saved to: {dest_path}")
        print(f"Dataset shape: {df.shape}")
        print(f"Sample intents: {df['intent'].unique()[:5]}")
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")

if __name__ == "__main__":
    download_bitext_telco()
