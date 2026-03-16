# Detailed Guides: Architecture & Security

This guide provides deep technical insights into how Repo Rosetta handles private repositories, maintains security, and integrates with local LLMs.

## 🌉 Private Repository Architecture
When you analyze a private repository, Repo Rosetta follows a strict security protocol:

1. **Authorization**: The user logs in via GitHub OAuth. The system verifies if the user has **Maintainer** permissions on the target repository.
2. **Ephemeral Ingestion**:
    - The backend clones the repository into a temporary, isolated directory.
    - The **Parser Engine** runs professional-grade AST extraction (supporting Python, JS, TS, TSX, Go, Rust, C++) to build the Knowledge Graph.
3. **Immediate Cleanup**: Once the Knowledge Graph is created, the raw source code is **permanently deleted** from the server's disk. Only the abstracted graph remains.
4. **Audit Logging**: Every analysis and view event is recorded in a tamper-proof audit log (found in `logs/audit`).

## 🛡 LLM Permission Gate
Repo Rosetta prevents accidental data egress to third-party cloud providers:

- **Public Repos**: Uses the default configured provider (Claude or Gemini).
- **Private Repos**: Analysis will **fail** unless the user explicitly selects a provider and consents to data transmission.
- **Local Alternative**: Users are encouraged to use **Ollama** for zero-cost, zero-egress private repo analysis.

## ⚙️ Environment Variable Management
All configuration for Repo Rosetta is managed via a `.env` file located in the project root.

1. **Create the file**: Copy `.env.example` to `.env`.
   ```bash
   cp .env.example .env
   ```
2. **Edit**: Open `.env` and fill in your keys. This file is ignored by Git to keep your secrets safe.

## 🐙 GitHub OAuth Setup (for Private Repos)
To enable private repository analysis, you must create a GitHub OAuth App:

1. **Go to GitHub Settings**: Navigate to [Developer Settings > OAuth Apps](https://github.com/settings/developers) and click **New OAuth App**.
2. **Details**:
   - **Application Name**: Repo Rosetta
   - **Homepage URL**: `http://localhost:3000`
   - **Authorization callback URL**: `http://localhost:3000/api/auth/callback`
3. **Credentials**:
   - Once created, copy the **Client ID**.
   - Click **Generate a new client secret** and copy it.
4. **Update `.env`**:
   ```env
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
   GITHUB_CALLBACK_URL=http://localhost:3000/api/auth/callback
   ```

## 🏗 Local LLM Configuration (Ollama)
For a 100% private and free experience, configure a local model:

1. **Install Ollama**: [Download here](https://ollama.ai/).
2. **Pull a model**:
   ```bash
   ollama pull deepseek-coder:6.7b
   ```
3. **Configure Docker**: Our `docker-compose.yml` includes an `ollama` service. To use your host's instance instead, update `NEXT_PUBLIC_OLLAMA_URL` to point to your local IP.
4. **Select Provider**: In the Explanation Panel, select **Ollama** as your preferred reasoning engine.

## 🧬 Architectural Regression Engine
Repo Rosetta's regression engine leverages `rustworkx` to perform high-speed graph diffing between repository states.
- **Goal**: Identify drift between the intended architecture and the implemented code.
- **Visualization**: When active, nodes are color-highlighted (Green: New, Amber: Changed) to show structural evolution.
- **CI/CD Integration**: The engine exposes a compare utility that can be used in CI pipelines to flag unauthorized architectural changes.

## 🔌 IDE Ecosystem (LSP Proxy)
The backend provides a standardized LSP (Language Server Protocol) proxy at `/api/lsp`.
- **Function**: Bridges the gap between the internal Knowledge Graph and external IDEs.
- **Metadata**: Returns hover insights and jump-to-definition mapping based on the architectural context rather than just local syntax.
- **Security**: Requires a valid OAuth token to fetch metadata for private repositories.

## 🐳 Self-Hosted Deployment
To run Repo Rosetta entirely within your own infrastructure:

```bash
# Set your environment variables
export GITHUB_CLIENT_ID=your_id
export GITHUB_CLIENT_SECRET=your_secret

# Start the stack
docker-compose up -d --build
```
This deploys the FastAPI backend, Next.js frontend, and a dedicated Ollama instance for a fully self-contained ecosystem.
