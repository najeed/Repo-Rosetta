# Repo Rosetta 📜✨

**Decode any codebase with interactive architecture maps and multi-persona AI explanations.**

Repo Rosetta transforms complex repositories into visual, understandable knowledge graphs. Whether you're a developer onboarding to a new project or an architect planning deep system changes, Rosetta provides the intelligence you need.

---

## ✨ Key Features

- **Interactive Architecture Maps**: Real-time visualization powered by React Flow with persistent team annotations.
- **Multi-Persona AI**: Tailored explanations for Beginner, Senior, Architect, and PM roles using multi-file context.
- **Context-Aware Intelligence**: RAG-driven insights using live repository data and local markdown documentation search.
- **Hardened Semantic Engine**: Production-grade Tree-sitter implementation for Python, JS, TS, TSX, Go, Rust, and C++.
- **LSP Evolution**: Integrated symbol lookup and hover metadata driven by the interactive knowledge graph.
- **Privacy-First**: Enterprise-grade permission gates and local LLM support for secure analysis.

---

## 🚀 Quick Start

### Docker (Recommended)
```bash
docker-compose up -d
```
Visit [http://localhost:3000](http://localhost:3000)

### CLI Scan
```bash
pip install -r backend/requirements.txt
python cli/rosetta.py ./your-repo --output ./docs/rosetta
```

---

## 📚 Documentation

For detailed guides, please refer to:

- **[Quickstart Guide](docs/guides/quickstart.md)**: Get up and running in minutes.
- **[Key Features & How-to](docs/guides/key_features.md)**: Personas, Maps, and Chat.
- **[Detailed Guides](docs/guides/detailed_guides.md)**: Security, Private Repos, and Ollama.
- **[User Documentation](docs/guides/user_documentation.md)**: Full installation and configuration reference.
- **[Feature Inventory & Roadmap](docs/guides/feature_inventory_and_roadmap.md)**: What's here and what's coming.

---

## 📜 License

Repo Rosetta is open-source software licensed under the **MIT License**.

---
*Built with ❤️ by [Najeed Khan](https://github.com/najeed) for developers who hate reading legacy code.*
