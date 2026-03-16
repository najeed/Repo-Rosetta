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
        approved_provider: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        if is_private and not approved_provider:
            raise PermissionError("Analysis of private repositories requires explicit LLM provider consent.")
        
        # Use approved provider if provided, otherwise default
        provider = approved_provider or self.provider
        api_key = os.getenv(f"{provider.upper()}_API_KEY")
        
        prompt = self._build_prompt(entity_data, persona, verbosity, context)
        
        # Real Provider Integration
        if api_key:
            try:
                if provider == "anthropic":
                    import anthropic
                    client = anthropic.AsyncAnthropic(api_key=api_key)
                    message = await client.messages.create(
                        model="claude-3-5-sonnet-latest",
                        max_tokens=1024,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return message.content[0].text
                
                elif provider == "gemini":
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    response = await model.generate_content_async(prompt)
                    return response.text
            except Exception as e:
                print(f"[*] LLM Provider error ({provider}): {e}. Falling back to base summary.")
        
        # Fallback to heuristic-based analyzer
        return self._generate_base_summary(entity_data, persona, verbosity)

    def _build_prompt(self, entity_data: Dict[str, Any], persona: str, verbosity: str, context: Optional[str] = None) -> str:
        # Construct the system and user prompts based on persona and verbosity
        base = f"Act as a {persona}. Explain this code at {verbosity} level: {entity_data}"
        if context:
            base += f"\n\nAdditional System Context (Dependencies/Relationships):\n{context}"
        return base

    def _generate_base_summary(self, entity_data: Dict[str, Any], persona: str, verbosity: str) -> str:
        """
        Generates a summary based on structured entity data, tailored to persona and verbosity.
        """
        name = entity_data.get("name", "unknown")
        type_ = entity_data.get("type", "entity")
        
        # Persona templates
        templates = {
            "beginner": {
                "scan": f"This is `{name}`, a {type_} that acts like a building block for the app.",
                "brief": f"`{name}` is a {type_} that helps the program do its job by handling specific tasks.",
                "standard": f"Basically, `{name}` is a {type_} that takes care of {type_}-related logic. It's like a specialized tool in a toolbox.",
                "deep": f"Let's look closely at `{name}`. It's a {type_} designed to stay simple while helping the whole system run smoothly."
            },
            "senior-engineer": {
                "scan": f"`{name}` ({type_}) - Core component in the current module's execution path.",
                "brief": f"This {type_} handles critical logic for {name}. It emphasizes modularity and clean separation of concerns.",
                "standard": f"Standard implementation of `{name}` ({type_}). It follows established patterns and ensures efficient data processing for this module.",
                "deep": f"Architectural deep dive into `{name}`: This {type_} is optimized for performance and maintainability. It utilizes efficient data structures to manage {type_} state."
            },
            "architect": {
                "scan": f"Entity `{name}`: Key architectural node with significant downstream dependencies.",
                "brief": f"`{name}` ({type_}) serves as a strategic interface for system-wide operations.",
                "standard": f"High-level analysis of `{name}`: This {type_} defines a core contract within the system's modular architecture.",
                "deep": f"Strategic evaluation of `{name}`: As a primary {type_}, it governs the flow of data between components, ensuring long-term system scalability."
            },
            "pm": {
                "scan": f"`{name}`: Feature component supporting the user dashboard logic.",
                "brief": f"The `{name}` {type_} provides essential capabilities for the project's roadmap items.",
                "standard": f"Business value of `{name}`: This {type_} enables key user-facing features and improves overall system reliability.",
                "deep": f"Strategic impact of `{name}`: This {type_} is a critical milestone for Phase 1-6 delivery, enabling enterprise-grade analytics."
            }
        }
        
        # Fallback to senior-engineer if persona not found
        persona_data = templates.get(persona, templates["senior-engineer"])
        return persona_data.get(verbosity, persona_data["standard"])
