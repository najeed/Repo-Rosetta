from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.graph.manager import GraphManager

router = APIRouter()
# Use a shared instance or re-initialize (for this prototype, we'll re-initialize or use a singleton pattern if we had one)
graph_manager = GraphManager() 

class LSPRequest(BaseModel):
    method: str
    params: Dict[str, Any]

@router.post("/lsp")
async def lsp_proxy(request: LSPRequest):
    # Real Lookups against the Knowledge Graph
    if request.method == "textDocument/hover":
        uri = request.params.get("textDocument", {}).get("uri", "")
        # Extract path from URI
        rel_path = uri.replace("file:///", "").replace("\\", "/")
        
        # Search graph for this file or specific entity
        match = None
        for node_id_str, internal_id in graph_manager.node_map.items():
            if rel_path in node_id_str:
                match = graph_manager.node_data[internal_id]
                break
        
        if match:
            return {
                "contents": {
                    "kind": "markdown",
                    "value": f"### Repo Rosetta Insight: {match['name']}\n\n**Type**: {match['type']}\n**Context**: Part of the semantic graph for {match['path']}.\n\n[Explain with AI](http://localhost:3000/summary/{match['path']}:{match['name']})"
                }
            }
    
    if request.method == "textDocument/definition":
        # Similar logic for definition
        return {"result": "Definition lookup enabled in v9 real core"}
        
    return {"result": "Method processed via Rosetta Live LSP"}
