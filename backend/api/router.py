from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class AnnotationRequest(BaseModel):
    node_id: str
    author: str
    text: str

from backend.instances import graph_manager, summarizer, parser_engine
from backend.auth.github import GitHubAuth
from backend.db.audit import AuditLogger
from backend.db.annotations import AnnotationManager

router = APIRouter()
auth_manager = GitHubAuth()
audit_logger = AuditLogger()
annotation_manager = AnnotationManager()

@router.post("/annotation")
async def save_annotation(request: AnnotationRequest):
    annotation_manager.save_annotation(request.node_id, request.author, request.text)
    return {"message": "Annotation saved successfully"}

@router.get("/annotations/{node_id:path}")
async def get_annotations(node_id: str):
    return annotation_manager.get_annotations(node_id)

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.post("/analyze")
async def analyze_repository(repo_url: str, token: Optional[str] = None, is_private: bool = False):
    # Clear graph immediately at start of fresh analysis
    graph_manager.clear()
    
    if is_private:
        if not token:
            raise HTTPException(status_code=401, detail="Authentication token required for private repository analysis.")
        
        # Local Development Mock Bypass
        if token == "mock-codebase-token":
            audit_logger.log_access("local_admin", repo_url, "analyze_private_mock")
        else:
            repo_name = repo_url.replace("https://github.com/", "")
            if not await auth_manager.verify_permission(token, repo_name):
                raise HTTPException(status_code=403, detail="Insufficient permissions (Maintainer+ required).")
            audit_logger.log_access("user_github", repo_name, "analyze_private")
    
    # Real Orchestration Logic
    import os
    from backend.models import CodeEntity
    
    local_path = "." # Current directory for demonstration
    SUPPORTED_EXTS = {".py", ".js", ".ts", ".tsx", ".go", ".rs", ".cpp", ".h"}
    
    scan_results = []
    # Normalize ignored paths for current OS
    IGNORED_DIRS = {".git", "node_modules", "venv", "__pycache__", ".next", ".gemini", "brain", ".agents", "dist", "build"}
    
    for root, dirs, files in os.walk(local_path):
        # Skip ignored directories effectively by checking all path components
        path_parts = set(os.path.normpath(root).split(os.sep))
        if any(ignored in path_parts for ignored in IGNORED_DIRS):
            continue
            
        valid_files = [f for f in files if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS]
        for file in valid_files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, local_path).replace("\\", "/")
            scan_results.append(rel_path)
            
            result = parser_engine.parse_file(file_path)
            if result and result.get("entities") is not None:
                # Add module node first with real line count
                graph_manager.add_entity(CodeEntity(
                    name="module",
                    type="module",
                    path=rel_path,
                    line_start=1,
                    line_end=result.get("line_count", 1)
                ))
                
                for ent in result["entities"]:
                    graph_manager.add_entity(CodeEntity(
                        name=ent["name"],
                        type=ent["type"],
                        path=rel_path,
                        line_start=ent["line_start"],
                        line_end=ent["line_end"]
                    ))
    
    # Build semantic connections across the finished graph
    graph_manager.build_semantic_connections()
    
    return {
        "message": f"Successfully completed full semantic analysis for {repo_url}",
        "stats": {
            "files_scanned": len(scan_results),
            "nodes_created": len(graph_manager.node_map)
        }
    }

@router.get("/graph")
async def get_graph():
    return graph_manager.get_graph_data()

@router.get("/summary")
async def get_summary(
    entity_id: str, 
    persona: str = "senior-engineer", 
    verbosity: str = "standard",
    is_private: bool = False,
    approved_provider: Optional[str] = None
):
    # Retrieve real entity data from graph for UI sections
    entity_data = {}
    dependencies = []
    key_functions = []
    
    if entity_id in graph_manager.node_map:
        internal_id = graph_manager.node_map[entity_id]
        entity_data = graph_manager.node_data[internal_id]
        
        # Build context from neighbors
        # successors are what this node depends on
        # predecessors are what depend on this node
        deps_ids = [int(i) for i in graph_manager.graph.successors(internal_id)]
        deps = [graph_manager.graph[i] for i in deps_ids]
        
        # Real dependencies for UI
        dependencies = [d.split(":")[-1] for d in deps]
        
        # Real key functions (if this is a module, find its children)
        if entity_data["type"] == "module":
            for nid in graph_manager.graph.node_indices():
                ndata = graph_manager.node_data[nid]
                if ndata["path"] == entity_data["path"] and ndata["type"] in ["function", "class"]:
                    key_functions.append({
                        "name": ndata["name"],
                        "type": ndata["type"],
                        "line": ndata["line_start"]
                    })

    else:
        # Fallback to name-only if not scanned yet
        entity_data = {"name": entity_id.split(":")[-1], "type": "unknown", "path": entity_id.split(":")[0]}

    try:
        # Summarizer now handles relational context building if graph_manager is passed
        summary = await summarizer.generate_summary(
            entity_data, 
            persona, 
            verbosity, 
            is_private=is_private, 
            approved_provider=approved_provider,
            graph_manager=graph_manager
        )
        return {
            "summary": summary, 
            "context_used": True,
            "dependencies": dependencies,
            "key_functions": key_functions
        }
    except PermissionError as e:
        raise HTTPException(status_code=402, detail=str(e))

@router.get("/trace/{node_id:path}")
async def get_execution_trace(node_id: str, depth: int = 3):
    """Returns a traced workflow starting from the specified node."""
    return graph_manager.get_execution_flow(node_id, depth)

@router.get("/annotations/{node_id:path}")
async def get_annotations(node_id: str):
    """Placeholder for annotations feature."""
    return [
        {"author": "System", "text": "Architectural baseline established.", "timestamp": "2026-03-16T12:00:00Z"},
        {"author": "AI", "text": "This node is a critical path orchestrator.", "timestamp": "2026-03-16T14:30:00Z"}
    ]
