# Repo Rosetta: User Documentation

Welcome to Repo Rosetta, the ultimate tool for decoding complex codebases through interactive architecture maps and multi-persona explanations.

---

## 🚀 Getting Started

### Installation (CLI)
The Rosetta CLI allows you to analyze repositories locally and generate documentation.

1. **Clone the repo**:
   ```bash
   git clone https://github.com/najeed/repo-rosetta.git
   cd repo-rosetta
   ```
2. **Setup environment**:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Run a scan**:
   ```bash
   python cli/rosetta.py /path/to/your/repo --output ./docs/rosetta
   ```

### Running the Web Dashboard (Docker)
For the full interactive experience, we recommend using Docker.

1. **Navigate to the root directory**.
2. **Start the stack**:
   ```bash
   docker-compose up -d
   ```
3. **Open your browser**: Navigate to `http://localhost:3000`.

---

## 🧠 Core Concepts

### Personas
Repo Rosetta explains code differently depending on your role:
- **Beginner**: Focuses on "What is this?" using simple analogies.
- **Senior Engineer**: High-density technical details, performance trade-offs, and design patterns.
- **Architect**: Focuses on system dependencies, data flow, and modular boundaries.
- **PM**: High-level functionality and business impact summaries.

### Verbosity Levels
- **Scan**: One-sentence high-level summary.
- **Brief**: Key functionality and primary dependencies.
- **Standard**: (Default) Logical flow and modular structure.
- **Deep**: Line-by-line mechanical analysis and edge-case handling.

---

## 🔒 Security & Privacy

### Private Repositories
Repo Rosetta is designed with a **Privacy-First** architecture:
- **Zero-Egress Analysis**: By using local LLMs (via Ollama), your private code never leaves your server.
- **Permission Gate**: The system will block cloud LLM analysis (Claude/Gemini) for private repos unless you explicitly approve a provider.
- **Secure Handling**: Raw source code is deleted immediately after the Knowledge Graph is constructed.
- **Audit Logging**: Every access to a private repository visualization is logged for security compliance.

### Authorization
- **Public Repos**: No login required. Just paste the GitHub URL.
- **Private Repos**: Requires a GitHub OAuth login and Maintainer permissions on the target repository.

---

## 🛠 LLM Configuration

Repo Rosetta supports multiple reasoning engines:

### 1. Cloud LLMs (Fastest & Deepest)
Set your API keys in the `.env` file in the project root (copied from `.env.example`).
- `ANTHROPIC_API_KEY`: For Claude 3.5 Sonnet.
- `GEMINI_API_KEY`: For Gemini 1.5 Pro.

### 2. GitHub OAuth (Private Repos)
To analyze private repositories, create an [OAuth App](https://github.com/settings/developers) on GitHub:
- **Callback URL**: `http://localhost:3000/api/auth/callback`
- Add the `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` to your `.env`.

### 2. Local LLMs (Free & Private)
Repo Rosetta integrates natively with **Ollama**.
- Install Ollama from [ollama.ai](https://ollama.ai).
- The system will automatically detect and route requests to `localhost:11434` if configured.
- Recommended models: `codellama`, `deepseek-coder`.

---

## 🏛 Ecosystem & Performance

### Multi-Language Support
Rosetta provides full AST-level mapping for:
- **Web**: JavaScript, TypeScript.
- **Systems**: Go, Rust, C++.
- **Scripting**: Python.

### High Performance Core
The graph engine is powered by **rustworkx**, a Rust-based library providing 10x-50x speedups for large dependency graphs compared to standard Python implementations.

### IDE Integration (LSP Proxy)
Rosetta provides an **LSP Proxy** endpoint at `/api/lsp`. This allows external editors (VS Code, JetBrains) to pull architectural insights (hover explanations, dependency paths) directly into your coding environment.

### Architectural Regression (CI/CD)
Track the "Drift" of your codebase. Rosetta can compare current graphs against baselines to highlight structural changes, ensuring that your architecture aligns with its documentation over time.

---

## ❓ FAQ & Troubleshooting

**Q: Why is my diagram empty?**
A: Ensure the repository path is correct and that it contains supported files ([.py](/cli/rosetta.py), `.js`, `.ts`).

**Q: My LLM is taking too long.**
A: If using local models, ensure you have sufficient RAM/GPU. For cloud models, check your API quota.

---
*For further assistance, please open an issue on the [Repo Rosetta GitHub](https://github.com/najeed/repo-rosetta).*
