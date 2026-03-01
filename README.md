# Omni-Resolve-Agentic 🚀

**Omni-Resolve-Agentic** is a state-of-the-art, multi-agent AI system designed for the telecommunications industry. Built using the **Google Agent Development Kit (ADK)** and the **Model Context Protocol (MCP)**, it provides a GDPR-compliant, scalable, and intelligent solution for customer service automation.

---

## 🏗️ Architecture

The system follows a hierarchical multi-agent architecture:

1.  **The ADK Brain (Orchestrator):** The root agent that analyzes incoming inquiries and delegates them to specialized experts.
2.  **Specialized Agents:**
    *   **Billing Expert:** Handles invoice disputes, payment status, and compensation.
    *   **Tech Support Expert:** Manages network troubleshooting, signal diagnostics, and outage reporting.
3.  **MCP Data Connectors (The Tools):** A unified interface connecting agents to:
    *   **Knowledge Base:** A searchable dataset of 26,000+ telecom-specific resolutions (from HuggingFace).
    *   **Billing DB:** Mock access to customer account balances and statuses.
    *   **Network Monitor:** Real-time (mocked) outage checking by ZIP code.
4.  **GDPR Utility:** A privacy layer that masks PII (Emails, Phone numbers) before data reaches the LLM.

---

## 🛠️ Tech Stack

*   **Framework:** Python 3.10+, [Google Agent Development Kit (ADK)](https://github.com/google/adk)
*   **LLM:** Vertex AI (Gemini 2.0 Flash)
*   **Connectivity:** [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
*   **Backend:** FastAPI & Uvicorn
*   **Frontend:** Vanilla CSS & HTML (Modern Chat Interface)
*   **Testing:** Pytest & HTTPX
*   **Deployment:** Docker & Google Cloud Run
*   **Data:** HuggingFace `bitext/Bitext-telco-llm-chatbot-training-dataset`

---

## 🚀 Getting Started

### 1. Prerequisites
*   [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda installed.
*   [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install) installed and authenticated.

### 2. Installation
Create and activate the environment:
```bash
conda create -n omni-resolve-agentic python=3.10 -y
conda activate omni-resolve-agentic
pip install -r requirements.txt
```

### 3. Google Cloud Setup (Personal Project)
Authenticate with your personal Google account:
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project [YOUR_PROJECT_ID]
gcloud services enable aiplatform.googleapis.com
```

### 4. Configuration
Create a `.env` file in the root directory:
```env
GOOGLE_CLOUD_PROJECT=your-personal-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

---

## 🧪 Testing

The system includes a comprehensive test suite covering privacy, data connectors, and API endpoints. Tests are automatically executed during the CI/CD process.

To run the tests locally:
```bash
pytest tests/
```

Test coverage includes:
- **GDPR Masking:** Ensures emails and phone numbers are correctly redacted.
- **MCP Tools:** Verifies data retrieval from billing and network tools.
- **API Integrity:** Validates endpoint availability and UI serving.

---

## ☁️ Deployment

The application is containerized and ready for **Google Cloud Run**.

### Local Build (Docker)
```bash
docker build -t omni-resolve-agentic .
docker run -p 8080:8080 --env-file .env omni-resolve-agentic
```

### Deploy to Cloud Run
```bash
gcloud run deploy omni-resolve-agentic \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=[YOUR_PROJECT_ID],GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

**Live URL:** [https://omni-resolve-agentic-285608224001.us-central1.run.app](https://omni-resolve-agentic-285608224001.us-central1.run.app)

---

## 📖 Usage

### Step 1: Download the Knowledge Base
Populate the local knowledge base with the telecom dataset:
```bash
python src/utils/download_data.py
```

### Step 2: Start the Web UI
Launch the FastAPI server:
```bash
python src/api.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📂 Project Structure

```text
├── data/               # Downloaded datasets (GIT IGNORED)
├── src/
│   ├── agents/         # ADK Agent definitions & Orchestrator
│   ├── tools/          # MCP Server & Tool implementations
│   ├── utils/          # GDPR masking & Data downloaders
│   ├── templates/      # UI HTML files
│   ├── api.py          # FastAPI Backend
│   └── main.py         # CLI Entry point
├── tests/              # Pytest suite
├── Dockerfile          # Container configuration
├── ARCHITECTURE.md     # Technical deep dive
├── requirements.txt    # Python dependencies
└── .env                # Environment secrets (GIT IGNORED)
```

---

## 🛡️ GDPR & Privacy
Privacy is baked into the core. The `src/utils/gdpr.py` utility automatically detects and masks:
*   **Emails:** `user@example.com` → `[EMAIL_MASKED]`
*   **Phone Numbers:** `+1 234 567 8900` → `[PHONE_MASKED]`

This happens **before** the inquiry is sent to the LLM orchestrator.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
