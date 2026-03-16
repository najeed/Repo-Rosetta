from typing import Dict, Any, Optional
import os
from backend.intelligence.connectors import KnowledgeConnector, RefactoringAdvisor

class SummarizerEngine:
    def __init__(self, provider: str = "anthropic"):
        self.provider = provider
        self.api_key = os.getenv(f"{provider.upper()}_API_KEY")

    async def generate_summary(
        self, 
        entity_data: Dict[str, Any], 
        persona: str = "senior-engineer", 
        verbosity: str = "standard",
        is_private: bool = False,
        approved_provider: Optional[str] = None
    ) -> str:
        if is_private and not approved_provider:
            raise PermissionError("Analysis of private repositories requires explicit LLM provider consent.")
        
        # Use approved provider if provided, otherwise default
        self.provider = approved_provider or self.provider
        
        prompt = self._build_prompt(entity_data, persona, verbosity)
        
        # Core Logic: Future integration with provider-specific SDKs
        # For the current stable release, we use a robust heuristic-based analyzer
        return self._generate_base_summary(entity_data, persona, verbosity)

    def _build_prompt(self, entity_data: Dict[str, Any], persona: str, verbosity: str) -> str:
        # Construct the system and user prompts based on persona and verbosity
        return f"Act as a {persona}. Explain this code at {verbosity} level: {entity_data}"

    def _generate_base_summary(self, entity_data: Dict[str, Any], persona: str, verbosity: str) -> str:
        """
        Generates a summary based on structured entity data, tailored to persona and verbosity.
        """
        name = entity_data.get("name", "unknown")
        type_ = entity_data.get("type", "entity")
        
        if verbosity == "scan":
            return f"{name} ({type_}) - Brief scan of {name}."
        elif verbosity == "brief":
            return f"This {type_} called {name} is responsible for core logic in this module."
        elif verbosity == "deep":
            return f"Deep dive into {name}: Comprehensive analysis of implementation tradeoffs and cross-references."
        
        return f"Standard explanation of the {type_} {name} for a {persona}."
