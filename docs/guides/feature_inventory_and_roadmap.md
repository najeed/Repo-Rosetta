# Repo Rosetta: Feature Inventory & Roadmap

## Feature Inventory (Status: Implemented)

### Core Analysis & Intelligence
- **Hardened Multi-Language Support**: AST-based extraction for Python, JS/TS, TSX, Go, Rust, and C++.
- **Knowledge Graph Management**: High-performance graph traversal using `rustworkx` (Rust-powered).
- **Multi-Persona Summarization**: Real-time context-aware explanations using live dependency data.
- **Dynamic Verbosity**: Depth control from "Scan" to "Deep".
- **Interactive Chat**: Context-aware RAG chat overlay for real-time codebase queries.
- **Enterprise Intelligence**:
    - **Internal Knowledge Integration**: Live local markdown search engine providing authentic internal documentation context.
    - **AI Refactoring Advisor**: Automated identification of architectural smells using semantic graph insights.
- **Resilience & Fallbacks**: Intelligent session-wide failure caching and intra-family model tiering (Pro -> Flash).

### Visualization & UX
- **Interactive Architecture Map**: React Flow diagrams with smooth panning/zooming.
- **Explanation Panel**: Rich detail sidebar with persona controls, refactoring tips, and external links.
- **Team Annotations**: Persistent, team-specific notes added via right-click on nodes.
- **Deep Linking**: Direct navigation from diagram nodes to GitHub source files.
- **Multi-Selection**: Bulk context analysis using shift-click selection.
- **Regression Mode**: Visual architectural diffing (Added/Modified) between commits.
- **Collaboration Presence**: View mock avatars of active team members.

### Ecosystem & IDE
- **LSP Proxy**: Standardized endpoint for IDE integrations (hover insights, jump-to-definition).
- **CI/CD Integration**: Utilities for architectural regression testing in pipelines.

### Security
- **Privacy-First**: Permission Gate for cloud LLMs on private repositories.
- **Secure Data Handling**: Ephemeral parsing and automatic raw code deletion.
- **Self-Hosted Mode**: Docker-ready stack including local LLM support via Ollama.

---

## Post-Launch Roadmap (Future)

### Automated Refactor Implementation
- **One-Click Refactors**: AI-driven PR generation for suggested architectural improvements.
- **Constraint Enforcement**: Define architectural "legal" and "illegal" deps that trigger CI failures.
