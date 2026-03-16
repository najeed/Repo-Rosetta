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

### Running the Web Dashboard

#### Option A: Docker (Recommended)
```bash
docker-compose up -d
```
Visit `http://localhost:3000`.

#### Option B: Native Local Launch
If you have Python and Node installed locally, use the provided scripts for a lighter setup:
- **Windows**: `run_local.bat`
- **macOS/Linux**: `chmod +x run_local.sh && ./run_local.sh`
Visit `http://localhost:3001`.

---

## 🧠 Core Concepts

### Personas
Repo Rosetta explains code differently depending on your role:
- **PM**: High-fidelity summaries focused on **impact, delivery, and business logic**. These summaries are extremely concise to respect the PM's time.
- **Senior Engineer**: In-depth technical analysis focused on **code quality, performance, maintainability, and idiomatic patterns**.
- **Architect**: Strategic evaluation focused on **design patterns (SOLID), modular boundaries, and system coupling**.
- **Beginner**: Focuses on "What is this?" using simple analogies and introductory-level explanations.

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
- The system automatically detects and routes requests to `localhost:11434`.
- **Recommended models**: `codellama`, `deepseek-coder:6.7b`, `llama3`.
- **Performance Note**: For local models, ensure you have **sufficient RAM (8GB+ for 7B models)** and a multi-core CPU or GPU. Faster execution requires dedicated VRAM (e.g., NVIDIA RTX or Apple Silicon).

### 3. LLM Resilience & Fallbacks
Rosetta is built to survive API failures and quota limits:
- **Intra-Family Fallback**: If a "Pro" model (like Gemini 2.5 Pro) fails, the engine automatically attempts a "Flash" or "Lite" version before moving to a different provider.
- **Format Awareness**: The engine detects if it's reading source code, metadata, git diffs, or logs, and adapts its prompts to match the content type.
- **Session-Wide Caching**: Failed models or exhausted providers are cached for your session, preventing redundant calls to broken endpoints and ensuring rapid failover to working resources like Ollama.

---

## 🎮 GUI Console Guide

The Repo Rosetta dashboard is divided into four main interactive zones:

### 1. The Architecture Map (Center)
- **Visualization**: A dynamic 2D/3D map of your codebase entities (modules, classes, functions).
- **Navigation**: Drag to pan, scroll to zoom.
- **Interactivity**: 
    - **Single Click**: Focus an entity to see its details in the right panel.
    - **Right-Click**: Add a **Persistent Note** (Team Note) to any node.
    - **Search (⌘K)**: Enter any term in the top-right search bar to highlight matching entities and dim others.

### 2. Explanation Panel (Right)
- **Instant Insights**: Displays the name, type, and line count of the selected entity.
- **Persona Switcher**: Choose between **Architect, Senior Engineer, PM, or Beginner** to change the tone and depth of the AI summary.
- **Verbosity Control**: Toggle between **Scan, Brief, Standard, and Deep** analysis.
- **Trace Execution**: If Debug mode is on, use "Trace" to see the calling flow for that entity.

### 3. Interactive Reasoning (Bottom-Right)
- Click the **Message Square** icon to open the chat overlay.
- Ask natural language questions like *"Where is the authentication logic?"* or *"How does the parser handle large files?"*.
- The AI uses the Knowledge Graph to provide high-fidelity, grounded answers.

### 4. Control Bar (Top)
- **Repo URL Input**: Enter a full GitHub URL (e.g., `https://github.com/user/repo`) and hit **ANALYZE** to trigger a fresh scan.
- **Public/Private Toggle**: Switch to Private mode to enable GitHub OAuth.
- **Debug Toggle**: Enables performance metrics, latency tracking, and execution tracing.

---

## 🔒 GitHub OAuth & Permissions

When analyzing **private repositories**, Repo Rosetta requires an OAuth token:
1. Toggle the **PUBLIC** badge to **PRIVATE**.
2. Click **Authorize with GitHub**.
3. In local development mode, this triggers a permissive authorization flow. For production, ensure `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are set in your `.env`.

---

## 🏛 Ecosystem & Performance

### Hardened Multi-Language Support
Rosetta provides production-grade AST-level mapping for:
- **Web**: JavaScript, TypeScript, TSX (React).
- **Systems**: Go, Rust, C++.
- **Scripting**: Python.

---

## ❓ FAQ & Troubleshooting

**Q: Why is my diagram empty?**
A: Ensure you have run **ANALYZE** after entering a repository URL. Check the terminal for backend errors if the scan fails.

**Q: Search isn't finding my file.**
A: The search bar highlights nodes already present in the graph. If a file isn't showing up, ensure it's a [supported type](file:///c:/Users/najee/OneDrive/Documents/Projects/Repo%20Rosetta/backend/api/router.py).

**Q: Chat says it can't connect.**
A: Ensure the backend is running (`uvicorn backend.main:app`). If the backend crashes, the chat overlay will show a connection error.

---
*For further assistance, please open an issue on the [Repo Rosetta GitHub](https://github.com/najeed/repo-rosetta).*
