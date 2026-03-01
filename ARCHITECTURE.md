# Omni-Resolve-Agentic: Architecture Deep Dive 🛠️

This document provides a detailed technical overview of the **Omni-Resolve-Agentic** codebase, explaining the design patterns, data flow, and multi-agent orchestration logic.

---

## 🏗️ High-Level Design

The system is built on four core pillars:
1.  **Orchestration:** Google Agent Development Kit (ADK).
2.  **Specialization:** Domain-specific LLM Agents.
3.  **Data Connectivity:** Model Context Protocol (MCP).
4.  **Privacy:** Deterministic PII Masking (GDPR).

### System Data Flow
1.  **User Input** → `src/api.py` (FastAPI)
2.  **Masking** → `src/utils/gdpr.py` (PII removal)
3.  **Routing** → `src/agents/orchestrator.py` (The ADK Brain)
4.  **Specialization** → `billing.py` or `tech_support.py`
5.  **Tooling** → `src/tools/mcp_server.py` (Data retrieval)
6.  **Response** → Synthesized result back to UI.

---

## 🧠 The ADK Brain (`src/agents/orchestrator.py`)

The **ADKBrain** is the root of the agent hierarchy. It uses the `Runner` pattern to manage state and delegation.

*   **Pattern:** Handoff/Routing.
*   **Logic:** It uses high-level instructions to analyze user intent. If the intent matches a specialist (defined in `cards.py`), it "transfers" the conversation.
*   **Key Class:** `InMemoryRunner`. It manages the `InvocationContext` and `Session`, ensuring history is maintained across turns.

---

## 👮 Specialized Agents (`src/agents/`)

Each specialist is an `LlmAgent` with a constrained domain:

*   **`billing.py`**: Instructed to focus on invoices and payments. It has exclusive access to the `get_billing_details` tool.
*   **`tech_support.py`**: Focused on network and hardware issues. It manages troubleshooting flows using the `search_knowledge_base` and `check_network_outage` tools.

All agents share a common metadata schema defined in `src/agents/cards.py` (The "Diplomat" pattern), ensuring consistent identification and discovery.

---

## 🔌 MCP Data Layer (`src/tools/mcp_server.py`)

We use the **Model Context Protocol (MCP)** via the `FastMCP` framework to decouple data retrieval from agent logic.

### 🔍 Semantic Search Tool
The `search_knowledge_base` tool is the most advanced component:
1.  **Pre-processing:** `src/utils/embed_data.py` uses Vertex AI (`text-embedding-004`) to convert telecom FAQs into 768-dimensional vectors.
2.  **Retrieval:** When a query arrives, it is embedded in real-time.
3.  **Similarity:** We use `cosine_similarity` (scikit-learn) to find the closest match in the vector space.
4.  **Thresholding:** A score > 0.6 is required for a Semantic Match; otherwise, it falls back to a Regex-based keyword search.

---

## 🛡️ GDPR & Security (`src/utils/gdpr.py`)

The system implements **"Privacy by Design"**:
*   The `mask_pii` function uses optimized regular expressions to catch sensitive patterns (Emails, Phone Numbers, Account IDs).
*   Masking happens at the **API Entry Point**, ensuring that raw PII never enters the LLM's context window or logs.

---

## 🧪 Verification & Testing

A robust test suite ensures stability across releases:
*   **Unit Tests (`tests/test_gdpr.py`):** Deterministic verification of PII redacting regex patterns.
*   **Tool Tests (`tests/test_mcp_tools.py`):** Functional testing of mock database retrievals and outage logic.
*   **Integration Tests (`tests/test_api.py`):** Validates the FastAPI routing and UI delivery.

Tests are executed using `pytest` and utilize `httpx` for asynchronous endpoint testing.

---

## ☁️ Infrastructure & Deployment

The system is designed for modern cloud-native environments:
*   **Containerization:** A multi-stage `Dockerfile` optimizes the image size while ensuring all C-extensions for `numpy` and `scikit-learn` are correctly compiled.
*   **Scalability:** Deployed on **Google Cloud Run**, providing an auto-scaling, serverless backend.
*   **Environment Management:** Managed via `.env` files and GCP Secret Manager-compatible environment variables.

---

## 📂 Codebase Map

| File | Responsibility |
| :--- | :--- |
| `src/api.py` | FastAPI server, served HTML UI, and `/chat` endpoint. |
| `src/main.py` | CLI-based test runner for debugging orchestration. |
| `src/agents/orchestrator.py` | The root ADK Brain and multi-agent management. |
| `src/agents/cards.py` | Metadata definitions for all agents (IDs, domains). |
| `src/tools/mcp_server.py` | Implementation of all MCP Tools (Search, Billing, Network). |
| `src/utils/gdpr.py` | PII masking logic for GDPR compliance. |
| `src/utils/embed_data.py` | Utility to generate vector embeddings for the KB. |
| `tests/` | Automated test suite. |
| `Dockerfile` | Container build configuration. |
| `data/` | CSV datasets and `.npy` vector storage (local only). |

---

## 🚀 Execution Model

The system operates **Asynchronously** (`async/await`) to handle streaming responses and concurrent tool calls. The `ADKBrain` iterates over an `AsyncGenerator` of events yielded by the ADK engine, allowing for future support of real-time streaming in the UI.
