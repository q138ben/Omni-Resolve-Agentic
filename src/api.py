from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from src.agents.orchestrator import create_adk_brain
from src.utils.gdpr import mask_pii

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Omni-Resolve-Agentic API")

# Initialize the ADK Brain once
brain = create_adk_brain()

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """
    Serves the modern chat interface.
    """
    template_path = os.path.join(os.getcwd(), "src", "templates", "index.html")
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")
    
    with open(template_path, "r") as f:
        return f.read()

@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    """
    GDPR-compliant chat endpoint that interacts with the ADK Brain.
    """
    try:
        # Step 1: GDPR PII Masking
        safe_query = mask_pii(request.query)
        
        # Step 2: ADK Brain Orchestration
        # This now triggers the real multi-agent engine asynchronously
        response_text = await brain.run(safe_query)
        
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
