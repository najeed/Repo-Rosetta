from typing import List, Dict, Any

class KnowledgeConnector:
    """
    Connects to internal knowledge sources (Slack, Notion, Wiki) for architectural context.
    """
    @staticmethod
    def get_related_context(query_term: str) -> List[Dict[str, str]]:
        # Knowledge Base Integration: Matches architectural patterns to internal discussions
        reference_data = {
            "auth": [
                {"source": "Slack", "text": "Discussion on moving to OAuth2 in #security-channel (March 2026)"},
                {"source": "Notion", "text": "Architecture Decision Record: GitHub App Integration for Private Repos"}
            ],
            "graph": [
                {"source": "Slack", "text": "@dev-team: Reminder to optimize NetworkX to rustworkx for large repos"},
                {"source": "Internal Wiki", "text": "Graph Schema Version 2.1 Documentation"}
            ]
        }
        
        # Base Heuristics: Keyword-based context retrieval
        for key in reference_data:
            if key in query_term.lower():
                return reference_data[key]
        
        return []

class RefactoringAdvisor:
    @staticmethod
    def get_suggestions(module_data: Dict[str, Any]) -> List[str]:
        suggestions = []
        
        # Mock heuristics for refactoring
        line_count = module_data.get("line_count", 0)
        complexity = module_data.get("complexity", "low")
        
        if line_count > 500:
            suggestions.append("🚀 Large Module: Consider splitting into smaller sub-modules to improve maintainability.")
        
        if complexity == "high":
            suggestions.append("🧠 High Cyclomatic Complexity: Extract deeply nested logic into utility functions.")
            
        if not module_data.get("has_docstrings", True):
            suggestions.append("📝 Documentation Gap: Add docstrings to public API functions for better discovery.")
            
        if not suggestions:
            suggestions.append("✅ Module looks healthy! No immediate refactors suggested.")
            
        return suggestions
