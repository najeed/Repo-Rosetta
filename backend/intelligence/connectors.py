from typing import List, Dict, Any

class KnowledgeConnector:
    """
    Connects to internal knowledge sources (Slack, Notion, Wiki) for architectural context.
    """
    @staticmethod
    def get_related_context(query_term: str) -> List[Dict[str, str]]:
        # Real-time Local Documentation Search
        # Scans the current repository for architectural context in markdown files
        context = []
        import os
        
        try:
            for root, _, files in os.walk("."):
                if any(ignored in root for ignored in [".git", "node_modules", "venv"]):
                    continue
                
                for file in files:
                    if file.lower().endswith(".md"):
                        path = os.path.join(root, file)
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            if query_term.lower() in content.lower():
                                # Extract a snippet
                                start_idx = content.lower().find(query_term.lower())
                                snippet = content[max(0, start_idx-50):min(len(content), start_idx+150)]
                                context.append({
                                    "source": os.path.relpath(path, ".").replace("\\", "/"),
                                    "text": f"...{snippet.strip()}..."
                                })
                                if len(context) >= 5: # Limit results
                                    return context
            return context
        except Exception as e:
            print(f"[*] KnowledgeConnector error: {e}")
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
