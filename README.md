# Repo Rosetta 📜✨

**Decode any codebase with interactive architecture maps and multi-persona AI explanations.**

Repo Rosetta transforms complex repositories into visual, understandable knowledge graphs. Whether you're a developer onboarding to a new project or an architect planning deep system changes, Rosetta provides the intelligence you need.

---

## ✨ Key Features

- **Interactive Architecture Maps**: Real-time visualization powered by React Flow with persistent team annotations.
- **Multi-Persona AI**: Tailored, high-fidelity explanations for **Senior Engineer** (code quality), **Architect** (system design), and **PM** (impact/concise).
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

### Local Setup (Non-Docker)
```bash
# 1. Setup .env
# Copy .env.example to .env and add your keys

# 2. Launch both Backend & Frontend
# On Windows:
run_local.bat

# On macOS/Linux:
chmod +x run_local.sh && ./run_local.sh
```
Visit [http://localhost:3000](http://localhost:3000) (or 3001 if 3000 is occupied)

### CLI Scan
```bash
python cli/rosetta.py ./your-repo --output ./docs/rosetta --debug
```
Use `--debug` to see LLM provider traces and latency.

---

## 🛠️ Performance & Resilience
Repo Rosetta is built for scale and transparency:
- **Map-Reduce Chunking**: Automatically handles multi-thousand line files by recursively summarizing logical chunks.
- **Ollama Optimization**: Native support for local models. *Note: Faster execution requires 8GB+ RAM and dedicated VRAM/GPU for 7B+ models.*
- **Zero-Wait Fallbacks**: Intelligent session-wide caching prevents redundant calls to failing providers, ensuring instant fallback to available resources.
- **Debug Mode**: Toggle the **DEBUG** switch in the UI to see real-time API performance and latency metrics in the browser console.
- **Execution Flow**: Click **Trace** on any module to see BFS-powered logic flows via the Knowledge Graph.

## 🧪 Health Verification
Ensure your environment is correctly configured by running the health check:
- **Windows**: `verify_health.bat`
- **macOS/Linux**: `chmod +x verify_health.sh && ./verify_health.sh`

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
