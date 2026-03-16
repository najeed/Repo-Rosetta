from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

router = APIRouter()

class LSPRequest(BaseModel):
    method: str
    params: Dict[str, Any]

@router.post("/lsp")
async def lsp_proxy(request: LSPRequest):
    # Mocking LSP JSON-RPC responses for IDE metadata
    if request.method == "textDocument/hover":
        path = request.params.get("textDocument", {}).get("uri", "")
        line = request.params.get("position", {}).get("line", 0)
        
        return {
            "contents": {
                "kind": "markdown",
                "value": f"### Repo Rosetta Insight\n\nThis module handles **core logic** at line {line}.\n\n[Open Architecture Map](http://localhost:3000?path={path})"
            }
        }
    
    if request.method == "textDocument/definition":
        return {
            "uri": "file:///mock/path/to/definition.py",
            "range": {"start": {"line": 10, "character": 0}, "end": {"line": 10, "character": 20}}
        }
        
    return {"result": "Method not implemented in mock Rosetta LSP"}
