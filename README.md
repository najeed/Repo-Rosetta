# Repo Rosetta 📜✨

**Decode any codebase with interactive architecture maps and multi-persona AI explanations.**

Repo Rosetta transforms complex repositories into visual, understandable knowledge graphs. Whether you're a developer onboarding to a new project or an architect planning deep system changes, Rosetta provides the intelligence you need.

---

## ✨ Key Features

- **Interactive Architecture Maps**: Powered by React Flow with multi-selection, team annotations, and **Regression Mode**.
- **Multi-Persona AI**: Tailored explanations for Beginner, Senior, Architect, and PM roles.
- **Interactive Chat (V3)**: Context-aware RAG conversation directly with your codebase.
- **Enterprise Intelligence (V5)**: AI Refactoring Advisor and Internal Knowledge base connectors (Slack/Notion).
- **Ecosystem Support (P6)**: LSP-style IDE proxy and **Architectural Regression Maps** for CI/CD visualization.
- **Privacy-First (V2)**: Permission gates and local LLM support (Ollama) for private repositories.
- **High Performance (V4)**: Rust-powered graph engine using `rustworkx` for 10x scalability.

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
- **[User Documentation](user_documentation.md)**: Full installation and configuration reference.
- **[Feature Inventory & Roadmap](feature_inventory_and_roadmap.md)**: What's here and what's coming.

---

## 📜 License

Repo Rosetta is open-source software licensed under the **MIT License**.

---
*Built with ❤️ for developers who hate reading legacy code.*
