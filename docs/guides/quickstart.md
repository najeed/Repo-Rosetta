# Quickstart Guide: Repo Rosetta

Welcome! This guide will get you from zero to architecture map in under 5 minutes.

## 1. Prerequisites
- **Python 3.9+** (for CLI/Backend)
- **Node.js 18+** (for Frontend)
- **Docker & Docker Compose** (Recommended for easiest setup)

## 2. Instant Setup (Docker)
The fastest way to experience Repo Rosetta is via Docker Compose.

```bash
git clone https://github.com/najeed/repo-rosetta.git
cd repo-rosetta
docker-compose up -d
```
Access the dashboard at [http://localhost:3000](http://localhost:3000).

## 3. Local CLI Scan
If you just want a quick `CODEBASE.md` file for your project:

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run the scan
python cli/rosetta.py ./my-project --output ./docs/rosetta
```

## 4. Analyzing Your First Repo
1. Open the Web Dashboard.
2. Enter a GitHub URL (e.g., `fastapi/fastapi`).
3. Click **Analyze**.
4. Explore the **Architecture Map** and click on any node to see a **Senior Engineer** explanation in the sidebar.
5. (Optional) Toggle **Regression Mode** in the top-right to see architectural diffs.

## 5. Next Steps
- Learn how to use [Personas and Verbosity](./key_features.md).
- Configure [Private Repository Access](./detailed_guides.md).
- Supported Languages: **Python, JavaScript, TypeScript, TSX, Go, Rust, and C++**.
