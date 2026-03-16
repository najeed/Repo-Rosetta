from typing import Dict, Any, Optional, List
import os
import asyncio
import random
import re
import httpx
from backend.intelligence.connectors import KnowledgeConnector, RefactoringAdvisor

class SummarizerEngine:
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        self.provider = provider
        self.default_model = model
        self.used_summaries = []
        self._available_ollama_models = []
        self._cached_providers = None
        self._failed_providers = {} # provider -> retry_at
        self._failed_models = set()
        
        # Persistent clients to ensure consistent settings (like max_retries)
        self._clients = {}
        self._init_clients()

    def _init_clients(self):
        """Initializes LLM clients with strict retry settings."""
        # OpenAI
        oa_key = os.getenv("OPENAI_API_KEY")
        if oa_key:
            try:
                from openai import AsyncOpenAI
                self._clients["openai"] = AsyncOpenAI(api_key=oa_key, max_retries=0)
            except Exception: pass
            
        # Anthropic
        an_key = os.getenv("ANTHROPIC_API_KEY")
        if an_key:
            try:
                from anthropic import AsyncAnthropic
                self._clients["anthropic"] = AsyncAnthropic(api_key=an_key, max_retries=0)
            except Exception: pass
            
        # Gemini (Using sync client as base; we'll use to_thread for async)
        ge_key = os.getenv("GEMINI_API_KEY")
        if self._is_valid_key(ge_key):
            try:
                from google import genai
                self._clients["gemini"] = genai.Client(api_key=ge_key)
                from backend.utils.logger import logger
                logger.debug("Summarizer", "Gemini client initialized successfully.")
            except Exception as e:
                from backend.utils.logger import logger
                logger.error("Summarizer", f"Failed to initialize Gemini client: {e}")
        elif ge_key:
            from backend.utils.logger import logger
            logger.warning("Summarizer", f"Gemini key skipped during client init (Invalid/Placeholder: {ge_key[:8]}...)")
    async def _discover_ollama_models(self):
        """Queries the local Ollama instance for installed models."""
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{ollama_host}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    self._available_ollama_models = [m["name"] for m in models]
        except Exception:
            pass # Silent failure for discovery

    def _is_valid_key(self, key: Optional[str]) -> bool:
        if not key or not isinstance(key, str): return False
        clean = key.strip()
        if not clean or len(clean) < 8: return False
        # Skip template values from .env.example
        low = clean.lower()
        if low.startswith("your_") or low.endswith("_here") or "api_key" in low: return False
        return True

    def _is_complex(self, entity_data: Dict[str, Any], verbosity: str) -> bool:
        """Determines if a task is 'complex' based on size, metadata, or verbosity."""
        if verbosity == "deep": return True
        
        raw_len = len(str(entity_data))
        if raw_len > 12000: return True
        
        metadata = entity_data.get("metadata", {})
        if metadata.get("out_degree", 0) > 5: return True
        if len(metadata.get("contained_entities", [])) > 10: return True
        
        return False

    def _get_model_tiers(self, provider: str, is_complex: bool) -> List[str]:
        """Returns a prioritized list of models within a provider family."""
        families = {
            "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
            "anthropic": ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-opus-latest"],
            "gemini": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
            "ollama": self._available_ollama_models or ["deepseek-coder:6.7b", "qwen2.5-coder", "llama3"]
        }
        
        # Legacy/Alias Mapping (To resolve 404s)
        mapping = {
            "gemini-1.5-pro": "gemini-1.5-pro-002",
            "gemini-1.5-flash": "gemini-1.5-flash-002",
            "gemini-3.1-pro": "gemini-2.5-pro", # Redirect deprecated previews
            "gemini-3.1-flash-lite": "gemini-2.5-flash-lite"
        }
        
        models = families.get(provider, [])
        if not models: return []
        
        # 1. Start with the base tiering
        if provider == "ollama" and self._available_ollama_models:
            # Implement Resolve logic from Decision Tree: Deepseek > Qwen > Llama
            prioritized = []
            for preferred in ["deepseek", "qwen", "llama", "codellama"]:
                for m in self._available_ollama_models:
                    if preferred in m.lower() and m not in prioritized:
                        prioritized.append(m)
            # Add remaining models
            for m in self._available_ollama_models:
                if m not in prioritized: prioritized.append(m)
        elif provider != "ollama":
            if is_complex:
                prioritized = list(models)
            else:
                prioritized = list(reversed(models))
        else:
            prioritized = list(models)

        # 2. Add environment override as the absolute first choice
        env_model = os.getenv(f"{provider.upper()}_MODEL")
        if env_model:
            # Apply mapping to env override too
            env_model = mapping.get(env_model, env_model)
            if env_model in prioritized:
                prioritized.remove(env_model)
            prioritized.insert(0, env_model)
            
        return prioritized

    def _get_available_providers(self, force_refresh: bool = False) -> List[str]:
        if not force_refresh and self._cached_providers is not None:
            return self._cached_providers

        # Requested Priority from Decision Tree: anthropic > gemini > openai > ollama
        candidates = ["anthropic", "gemini", "openai", "ollama"]
        available = []
        
        import time
        for p in candidates:
            # Check for transient failure recovery
            if p in self._failed_providers:
                if time.time() < self._failed_providers[p]:
                    continue
                else:
                    del self._failed_providers[p] # Retry allowed
            
            if p == "ollama":
                ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
                if ollama_host: 
                    available.append(p)
                else:
                    from backend.utils.logger import logger
                    logger.warning("Summarizer", "OLLAMA_HOST not found. Skipping Ollama.")
            else:
                key = os.getenv(f"{p.upper()}_API_KEY")
                if self._is_valid_key(key):
                    available.append(p)
                elif key:
                    from backend.utils.logger import logger
                    logger.warning("Summarizer", f"Provider '{p}' skipped: API key is invalid or placeholder ('{key[:10]}...')")
                else:
                    from backend.utils.logger import logger
                    logger.debug("Summarizer", f"Provider '{p}' skipped: No API key found.")
        
        # self._cached_providers = available # Disable caching to pick up .env changes during dev
        return available

    async def generate_summary(
        self, 
        entity_data: Dict[str, Any], 
        persona: str = "senior-engineer", 
        verbosity: str = "standard",
        is_private: bool = False,
        approved_provider: Optional[str] = None,
        context: Optional[str] = None,
        model: Optional[str] = None,
        graph_manager: Optional[Any] = None
    ) -> str:
        from backend.utils.logger import logger
        import time
        
        # 1. Automatic Context Enhancement (Logic Unification)
        if graph_manager and not context:
            context = self._enhance_context(entity_data, graph_manager)

        if is_private and not approved_provider:
            raise PermissionError("Analysis of private repositories requires explicit LLM provider consent.")
        
        available = self._get_available_providers()
        primary = approved_provider or self.provider
        
        # Determine priority list: User-selection first, then Rank-based fallbacks
        priority_list = []
        if primary:
            # If primary is available, put it first
            if primary in available:
                priority_list.append(primary)
                for p in available:
                    if p != primary: priority_list.append(p)
            else:
                # If primary was explicitly asked for but not in 'available' (e.g. invalid key)
                # we still try it if it's not heuristic, just in case
                if primary != "heuristic":
                    priority_list.append(primary)
                priority_list.extend([p for p in available if p != primary])
        else:
            priority_list = list(available)
        
        from backend.utils.logger import logger
        logger.debug("Summarizer", f"Strategy: Primary='{primary}', Available={available}, PriorityList={priority_list}")

        # Intelligent Fallback & Tiering Loop
        res = None
        used_provider = "heuristic"
        used_model = "template-v1"
        
        start_time = time.time()
        is_complex = self._is_complex(entity_data, verbosity)
        
        for provider in priority_list:
            # Get tiered models for this provider
            target_models = [model] if (model and provider == approved_provider) else self._get_model_tiers(provider, is_complex)
            
            # Filter out models that have failed globally in this session
            target_models = [m for m in target_models if m not in self._failed_models]
            
            for t_model in target_models:
                try:
                    raw_data = str(entity_data)
                    threshold = 16000
                    
                    if len(raw_data) > threshold and provider != "gemini":
                        logger.info("Summarizer", f"Large entity. Map-Reduce with {provider} ({t_model})")
                        chunks = self._chunk_text(raw_data, threshold)
                        chunk_summaries = []
                        for chunk in chunks:
                            c_res = await self._call_llm(provider, t_model, f"Summarize: {chunk}")
                            if c_res: chunk_summaries.append(c_res)
                        
                        if chunk_summaries:
                            synth_prompt = f"Synthesize into {verbosity} for {persona}:\n" + "\n".join(chunk_summaries)
                            res = await self._call_llm(provider, t_model, synth_prompt)
                    else:
                        logger.log_trace("Summarizer", f"Attempting {provider} ({t_model})", provider, t_model)
                        res = await self._call_llm(provider, t_model, self._build_prompt(entity_data, persona, verbosity, context))
                    
                    if res:
                        used_provider = provider
                        used_model = t_model
                        break # Success with this model!
                        
                except Exception as e:
                    logger.error("Summarizer", f"Model {t_model} on {provider} failed: {e}. Trying next tier/provider...")
                    # If it's a quota error (429) or other terminal error, cache the model failure
                    err_str = str(e).lower()
                    if "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str or "limit" in err_str:
                        logger.warning("Summarizer", f"Model {t_model} is exhausted. Skipping for this session.")
                        self._failed_models.add(t_model)
                    continue
            
            if res:
                break # Success with this provider!
            
            # If we reached here, this provider failed all its models
            logger.error("Summarizer", f"All models for provider {provider} failed. Marking as failed for 5 mins.")
            self._failed_providers[provider] = time.time() + 300 # 5 minute cooldown
        latency = time.time() - start_time
        logger.log_trace("Summarizer", "Summarization cycle complete", used_provider, used_model, latency)
        
        is_heuristic = False
        if not res:
            logger.warning("Summarizer", "All LLM providers failed or none configured. Using heuristic fallback.")
            res = self._generate_base_summary(entity_data, persona, verbosity)
            is_heuristic = True

        # Quality Scoring
        try:
            from backend.summarizer.quality import QualityScorer
            contained = entity_data.get("metadata", {}).get("contained_entities", [])
            symbols = [e.get("name") for e in contained]
            score = QualityScorer.calculate_score(res, self.used_summaries[-10:], symbols, is_heuristic=is_heuristic)
            critique = QualityScorer.get_critique(score)
            logger.info("Summarizer", f"Quality Check: {score}/100 - {critique}")
            self.used_summaries.append(res)
        except Exception: pass
            
        return res

    def _chunk_text(self, text: str, size: int) -> List[str]:
        return [text[i:i+size] for i in range(0, len(text), size)]

    async def _call_llm(self, provider: str, model: str, prompt: str) -> Optional[str]:
        from backend.utils.logger import logger
        if provider == "heuristic": 
            return None
            
        client = self._clients.get(provider)
        if not client and provider != "ollama":
            # Lazy re-init in case env changed
            self._init_clients()
            client = self._clients.get(provider)
        
        if provider == "openai" and client:
            try:
                response = await client.chat.completions.create(
                    model=model, messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error("Summarizer", f"OpenAI call failed: {e}")
                return None
            
        elif provider == "anthropic" and client:
            try:
                response = await client.messages.create(
                    model=model, max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            except Exception as e:
                logger.error("Summarizer", f"Anthropic call failed: {e}")
                return None
        
        elif provider == "gemini" and client:
            try:
                # Use to_thread to safely call the sync Client methods in an async way
                def _sync_call():
                    return client.models.generate_content(model=model, contents=prompt)
                
                response = await asyncio.to_thread(_sync_call)
                return response.text
            except Exception as e:
                logger.error("Summarizer", f"Gemini call failed: {e}")
                return None
        
        elif provider == "ollama":
            try:
                ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
                async with httpx.AsyncClient(timeout=300.0) as h_client:
                    response = await h_client.post(
                        f"{ollama_host}/api/generate",
                        json={"model": model, "prompt": prompt, "stream": False}
                    )
                    if response.status_code == 200:
                        return response.json().get("response")
                    else:
                        raise Exception(f"Ollama Error: Status {response.status_code}")
            except Exception as e:
                logger.error("Summarizer", f"Ollama call failed: {e}")
                return None
        
        return None

    def _detect_format(self, data: Any) -> str:
        """Detects the input format to tailor prompting."""
        import re
        if isinstance(data, dict): return "structural_metadata"
        if not isinstance(data, str): return "unknown"
        
        stripped = data.strip()
        if stripped.startswith("diff --git") or stripped.startswith("Index:") or ("--- a/" in stripped and "+++ b/" in stripped):
            return "git_diff"
        if re.search(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}", stripped):
            return "log_data"
        return "source_code"

    def _build_prompt(self, entity_data: Any, persona: str, verbosity: str, context: Optional[str] = None) -> str:
        fmt = self._detect_format(entity_data)
        role = "GENERAL_MODULE"
        if isinstance(entity_data, dict):
            role = self._classify_role(entity_data)
        
        instructions = [
            f"Act as a {persona}.",
            f"Goal: Provide a high-fidelity summary of this code entity at a '{verbosity}' level.",
            f"Entity Role: {role} (Topological Classification)",
        ]
        
        if fmt == "structural_metadata":
            instructions.append("Input: You are receiving structural representation of a code file (metadata).")
        elif fmt == "git_diff":
            instructions.append("Input: You are receiving a git diff showing changes to the codebase.")
        elif fmt == "log_data":
            instructions.append("Input: You are receiving system/application logs.")
        else:
            instructions.append("Input: You are receiving the raw source code for a module.")
            
        instructions.extend([
            "IMPORTANT: Do NOT critique the input format. Simply interpret the content as a factual representation of the codebase's current state or history.",
            "Your summary must be professional, technical, and focused on providing actionable insights."
        ])
        
        # Persona Specialization
        if persona == "pm":
            instructions.append("PM PERSPECTIVE: Focus on delivery, business impact, and external dependencies. Be extremely concise.")
        elif persona == "architect":
            instructions.append("ARCHITECT PERSPECTIVE: Focus on system boundaries, modularity, design patterns (SOLID), and coupling. Evaluate strategic health.")
        elif persona == "senior-engineer":
            instructions.append("ENGINEER PERSPECTIVE: Focus on code quality, performance, complexity, idiomatic patterns, and maintainability. Identify technical debt.")

        prompt = "\n".join(instructions)
        input_label = {
            "structural_metadata": "Entity Metadata",
            "git_diff": "Git Diff Content",
            "log_data": "Log Data Entries",
            "source_code": "Source Code Content"
        }.get(fmt, "Content")
        
        prompt += f"\n\n{input_label}:\n{entity_data}"
       
        if context:
            prompt += f"\n\nSystem Relationship Context:\n{context}"
        
        return prompt

    def _classify_role(self, data: Dict[str, Any]) -> str:
        name = data.get("name", "").lower()
        path = data.get("path", "").lower()
        out_deg = data.get("metadata", {}).get("out_degree", 0)
        in_deg = data.get("metadata", {}).get("in_degree", 0)
        
        if "api/" in path or "router" in name: return "CONTROLLER"
        if "model" in name or "schema" in name: return "DATA_MODEL"
        if out_deg > 3 and in_deg > 3: return "CORE_ENGINE"
        if in_deg > 5: return "UTILITY_LIB"
        if out_deg == 0 and in_deg == 0: return "ISOLATED_SCRIPT"
        return "GENERAL_MODULE"

    def _generate_base_summary(self, entity_data: Dict[str, Any], persona: str, verbosity: str) -> str:
        name = entity_data.get("name", "unknown")
        type_ = entity_data.get("type", "entity")
        role = self._classify_role(entity_data)
        
        metadata = entity_data.get("metadata", {}) or {}
        contained = metadata.get("contained_entities", [])
        out_deg = metadata.get("out_degree", 0)
        in_deg = metadata.get("in_degree", 0)
        
        contained_summary = ""
        if contained:
            by_type = {}
            for e in contained[:10]:
                t = e.get("type", "entity")
                if t not in by_type: by_type[t] = []
                by_type[t].append(f"`{e.get('name')}`")
            parts = [f"{t.capitalize()}s: {', '.join(names)}" for t, names in by_type.items()]
            contained_summary = " Internally, it implements: " + "; ".join(parts) + "."

        phrases = {
            "CONTROLLER": {
                "opener": [f"The `{name}` controller facilitates system interactions", f"`{name}` serves as a traffic router"],
                "rationale": "It bridges external requests with internal business logic."
            },
            "CORE_ENGINE": {
                "opener": [f"`{name}` is a central orchestrator", f"The `{name}` engine powers core workflows"],
                "rationale": "As a highly-connected node, it coordinates state across multiple subsystems."
            },
            "DATA_MODEL": {
                "opener": [f"`{name}` defines the data contract", f"Structure of `{name}` focuses on state definition"],
                "rationale": "It ensures type safety and consistency for data-at-rest and in-transit."
            },
            "UTILITY_LIB": {
                "opener": [f"`{name}` provides reusable utilities", f"`{name}` centralizes common helper logic"],
                "rationale": "It simplifies code by abstracting away repetitive, low-level operations."
            },
            "ISOLATED_SCRIPT": {
                "opener": [f"`{name}` is a standalone task script", f"The `{name}` script performs discrete operations"],
                "rationale": "It is designed for execution outside the main service loop."
            },
            "GENERAL_MODULE": {
                "opener": [f"`{name}` encapsulates domain-specific logic", f"`{name}` is a modular component"],
                "rationale": "It contributes to the overall system coherence by isolating specific concerns."
            }
        }

        role_data = phrases.get(role, phrases["GENERAL_MODULE"])
        import random
        random.seed(len(name) + out_deg)
        opener = random.choice(role_data["opener"])
        rationale = role_data["rationale"]

        if persona == "architect":
            opener = f"Strategic evaluation: {opener}."
            rationale = f"From an architectural perspective, {rationale[0].lower()}{rationale[1:]} It maintains strategic boundaries through clear encapsulation."
        if persona == "senior-engineer":
            opener = f"Technical analysis: {opener}."
            rationale = f"From an engineering perspective, {rationale[0].lower()}{rationale[1:]} Implementation details suggest a focus on {random.choice(['readability', 'robustness', 'performance'])}."
        elif persona == "pm":
            opener = f"Impact Analysis: {opener}."
            rationale = f"This directly supports feature stability by {rationale[0].lower()}{rationale[1:]} It reduces cross-team friction by isolating concerns."

        if verbosity == "brief":
            return opener
        
        res = f"{opener} {rationale}"
        if verbosity in ["standard", "deep"]:
            res += f" **Implementation Details**: {contained_summary or 'Standard structural wrapper.'}"
        
        if verbosity == "deep":
            res += f" Mechanically, this node supports {out_deg} outgoing integrations and is referenced by {in_deg} components."
            
        return res

    def _enhance_context(self, entity_data: Dict[str, Any], graph_manager: Any) -> str:
        """Shared logic to build rich architectural context for an entity."""
        name = entity_data.get("name", "entity")
        path = entity_data.get("path", "")
        type_ = entity_data.get("type", "unknown")
        
        context = f"Analyzing {type_} '{name}' in path '{path}'.\n"
        
        # 1. Relational Context
        metadata = entity_data.get("metadata", {})
        in_deg = metadata.get("in_degree", 0)
        out_deg = metadata.get("out_degree", 0)
        
        if in_deg > 5:
            context += "- This is a highly-reused component (utility/library block).\n"
        if out_deg > 5:
            context += "- This component has many external dependencies (orchestrator block).\n"

        # 2. Child Discovery (Functional Unification)
        # If it's a module, find all functions and classes inside it
        if type_ == "module" and hasattr(graph_manager, "node_data"):
            children = []
            for _, other_id in getattr(graph_manager, "node_map", {}).items():
                other_data = graph_manager.node_data[other_id]
                if other_data.get("path") == path and other_data.get("type") != "module":
                    children.append(f"- {other_data.get('type')}: `{other_data.get('name')}`")
            
            if children:
                context += "Detailed internal structure:\n" + "\n".join(children[:15]) + "\n"
        
        # 3. Dependencies
        deps = entity_data.get("dependencies", [])
        if deps:
            context += f"Direct dependencies: {', '.join(deps)}.\n"
            
        return context
