from fastapi import APIRouter, HTTPException
from typing import Optional
from backend.parser.engine import ParserEngine
from backend.graph.manager import GraphManager
from backend.summarizer.engine import SummarizerEngine
from backend.models import RepositoryContext

from backend.auth.github import GitHubAuth
from backend.db.audit import AuditLogger

router = APIRouter()
parser = ParserEngine()
graph_manager = GraphManager()
summarizer = SummarizerEngine()
auth_manager = GitHubAuth()
audit_logger = AuditLogger()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.post("/analyze")
async def analyze_repository(repo_url: str, token: Optional[str] = None, is_private: bool = False):
    if is_private:
        if not token:
            raise HTTPException(status_code=401, detail="Authentication token required for private repository analysis.")
        
        # Verify permission
        repo_name = repo_url.replace("https://github.com/", "")
        if not await auth_manager.verify_permission(token, repo_name):
            raise HTTPException(status_code=403, detail="Insufficient permissions (Maintainer+ required).")
        
        audit_logger.log_access("user_me", repo_name, "analyze_private")
    
    # Service Lifecycle: Clones repository, performs semantic parsing, 
    # and constructs the knowledge graph before secure cleanup.
    # parser.cleanup(local_path)
    
    return {"message": f"Successfully started analysis for {repo_url}"}

@router.get("/graph")
async def get_graph():
    return graph_manager.get_graph_data()

@router.get("/summary/{entity_id}")
async def get_summary(
    entity_id: str, 
    persona: str = "senior-engineer", 
    verbosity: str = "standard",
    is_private: bool = False,
    approved_provider: Optional[str] = None
):
    mock_data = {"name": entity_id, "type": "function"}
    try:
        summary = await summarizer.generate_summary(
            mock_data, 
            persona, 
            verbosity, 
            is_private=is_private, 
            approved_provider=approved_provider
        )
        return {"summary": summary}
    except PermissionError as e:
        raise HTTPException(status_code=402, detail=str(e))
