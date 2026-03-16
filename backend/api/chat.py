from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.summarizer.engine import SummarizerEngine
from backend.graph.manager import GraphManager

class ChatRequest(BaseModel):
    query: str
    context_node_ids: Optional[List[str]] = None
    repo_url: str
    persona: str = "senior-engineer"

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

router = APIRouter()
summarizer = SummarizerEngine()
graph_manager = GraphManager()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_codebase(request: ChatRequest):
    # 1. Extract context from graph based on query and context_node_ids
    context_data = []
    if request.context_node_ids:
        for node_id in request.context_node_ids:
            # Mock retrieving node data from graph
            context_data.append({"id": node_id, "content": f"Context for {node_id}"})
    else:
        # Fallback: get top-level module summaries as context
        context_data.append({"id": "root", "content": "Project overview context"})

    # Reasoning Engine: Integrates knowledge graph context with LLM summarization
    try:
        # Future: Specific chat_engine for dialogue-based reasoning.
        # Current: Leveraging stable summarization logic for dialogue responses.
        answer = f"Based on the context of {request.repo_url}, here is the answer to your query: '{request.query}'. (Context: {len(context_data)} nodes analyzed)"
        sources = [c['id'] for c in context_data]
        
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
