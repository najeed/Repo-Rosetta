from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.summarizer.engine import SummarizerEngine
from backend.graph.manager import GraphManager
import os

class ChatRequest(BaseModel):
    query: str
    context_node_ids: Optional[List[str]] = None
    repo_url: str
    persona: str = "senior-engineer"

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

from backend.instances import graph_manager, summarizer
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_codebase(request: ChatRequest):
    # 1. Identify context nodes using query if not explicitly provided
    context_nodes = request.context_node_ids or graph_manager.find_relevant_nodes(request.query)
    
    if not context_nodes:
        return ChatResponse(
            answer="I couldn't find any specific code entities related to your query in the current graph. Could you please try rephrasing or running a full scan?",
            sources=[]
        )

    # 2. Gather structural context for each relevant node
    full_reasoning_context = []
    for node_id in context_nodes:
        full_reasoning_context.append(graph_manager.get_node_context(node_id))
    
    context_str = "\n".join(full_reasoning_context)
    
    # 3. Formulate the reasoning prompt
    prompt = (
        f"You are a code reasoning assistant for the repository '{request.repo_url}'.\n"
        f"The user persona is '{request.persona}'.\n\n"
        f"Here is the structural context from the Knowledge Graph:\n"
        f"--- CONTEXT START ---\n{context_str}\n--- CONTEXT END ---\n\n"
        f"User Query: {request.query}\n\n"
        f"Answer the user's query precisely, citing the node names (e.g. `path:name`) provided in the context."
    )

    try:
        # 4. Generate answer using the summarizer's multi-provider engine (with chunking support)
        # We reuse the summarizer's _call_llm which handles provider selection and discovery
        available = summarizer._get_available_providers()
        provider = available[0] if available else "heuristic"
        
        # Use target model logic similar to engine.py
        target_model = os.getenv("GEMINI_MODEL", "gemini-1.5-pro") if provider == "gemini" else None
        
        answer = await summarizer._call_llm(provider, target_model or "heuristic", prompt)
        
        if not answer:
            answer = f"I analyzed {len(context_nodes)} modules but couldn't generate a high-fidelity reasoning response. The relevant modules appear to be: {', '.join(context_nodes)}."
            
        return ChatResponse(answer=answer, sources=context_nodes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
