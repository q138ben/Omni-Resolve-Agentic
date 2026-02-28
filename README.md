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

## 📖 Usage

### Step 1: Download the Knowledge Base
Populate the local knowledge base with the telecom dataset:
```bash
python src/utils/download_data.py
```

### Step 2: Run the CLI Test
Verify the orchestration and tools without the UI:
```bash
python src/main.py
```

### Step 3: Start the Web UI
Launch the FastAPI server and open [http://localhost:8000](http://localhost:8000):
```bash
python src/api.py
```

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
├── gemini.md           # Core Project Context
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
