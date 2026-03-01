# Development & Operations Guide 🛠️

This guide explains how to verify, test, and deploy the **Omni-Resolve-Agentic** system.

---

## 🧪 Testing Guide

The project uses `pytest` for automated testing. 

### 1. Setup Test Environment
Ensure you have the testing dependencies installed:
```bash
pip install pytest pytest-asyncio httpx
```

### 2. Running Tests
Run the entire suite from the root directory:
```bash
pytest tests/
```

### 3. Test Categories
*   **Privacy Verification (`tests/test_gdpr.py`):** Checks the regex-based PII masking. If you add new PII patterns (e.g., Credit Card numbers), add a test case here.
*   **Tool Verification (`tests/test_mcp_tools.py`):** Ensures the MCP server correctly interacts with mock data and the Knowledge Base.
*   **API Verification (`tests/test_api.py`):** Uses `FastAPI.TestClient` to ensure the web server starts and routes requests correctly.

---

## ☁️ Deployment Guide (Google Cloud)

The system is designed to run on **Google Cloud Run** using containerization.

### 1. Pre-Deployment Checklist
Before deploying, you must generate the local data artifacts:
1.  **Download Data:** `python src/utils/download_data.py`
2.  **Generate Embeddings:** `python src/utils/embed_data.py`
These generate the `.csv` and `.npy` files required by the Docker image.

### 2. Containerization (Docker)
The `Dockerfile` handles the environment setup. You can test it locally:
```bash
# Build the image
docker build -t omni-resolve-agentic .

# Run locally (uses your local .env)
docker run -p 8080:8080 --env-file .env omni-resolve-agentic
```

### 3. Deploying to Cloud Run
Use the following command to build and deploy in one step via **Cloud Build**:

```bash
gcloud run deploy omni-resolve-agentic 
  --source . 
  --region us-central1 
  --project [YOUR_PROJECT_ID] 
  --allow-unauthenticated 
  --set-env-vars GOOGLE_CLOUD_PROJECT=[YOUR_PROJECT_ID],GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

### 4. Continuous Integration (Optional)
For a production workflow, you can connect your GitHub repository to Cloud Run:
1. Go to the [Cloud Run Console](https://console.cloud.google.com/run).
2. Click **"Set up Continuous Deployment"**.
3. Link your GitHub repo and select the `main` branch.
4. Cloud Run will automatically run `pytest` (if configured in a pipeline) and redeploy on every push.

---

## 🔧 Troubleshooting

### Build Failures
If the Docker build fails on Cloud Run:
*   Ensure all files in `data/` exist. The Dockerfile copies the entire `data/` folder.
*   Check the **Cloud Build logs** in the GCP Console for specific Python pip installation errors.

### 404 Model Not Found
If the API returns a 404 regarding Gemini:
*   Ensure the `MODEL_NAME` in `src/agents/orchestrator.py` is a currently supported stable version (e.g., `gemini-2.0-flash`).
*   Verify that the **Vertex AI API** is enabled in your project.
