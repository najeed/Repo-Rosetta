# Key Features of Repo Rosetta

Master the intelligence and navigation features of Repo Rosetta to get the most out of your codebase analysis.

## 🎭 Using Personas
Repo Rosetta's AI can shift its perspective to match your needs. Use the **Persona Selector** in the Explanation Panel:

- **PM**: High-fidelity summaries focused on **impact and business logic**. Extremely concise.
- **Senior Engineer**: Technical depth focused on **code quality, maintainability, and performance**.
- **Architect**: Strategic perspective: **SOLID patterns, modularity, and system boundaries**.
- **Beginner**: High-level introductions using simple language and analogies.
## 📏 Adjusting Verbosity
Control the detail of the explanations using the **Verbosity Slider**:

1. **Scan**: A one-line summary. Perfect for rapid browsing of many modules.
2. **Brief**: Highlights the 2-3 most important responsibilities of the code.
3. **Standard**: Detailed overview of internal logic and direct dependencies.
4. **Deep**: Exhaustive analysis, including edge cases and line-by-line mechanics.

## 🗺 Interactive Maps (Web UI)
The **Interactive Architecture Maps**: Real-time visualization powered by **React Flow** and **D3.js** with persistent team annotations.
- **Map-Reduce Chunking**: Effortlessly analyze multi-thousand line files. Rosetta semantically splits massive modules and recursively synthesizes them into cohesive summaries.
- **Execution Flow Tracing**: Click "Trace" on any node to perform a BFS-powered logic audit, revealing hidden connections across your repository.
- **Internal Knowledge Graph**: All features are backed by a unified semantic index, ensuring consistent reasoning across visual and chat interfaces.
- **Hierarchy**: Use the **Layout Toggle** to switch between "Logical/Folder" views and "Dependency" views.
- **MiniMap**: Use the bottom-right MiniMap to navigate large-scale codebases without losing context.

## 🐚 CLI & Markdown Reports
For portability, the CLI generates **Mermaid** diagrams (`graph TD`) which can be natively rendered by GitHub, VS Code, and Obsidian. This ensures your documentation remains useful even when viewed in a static markdown environment.

## 💬 Interactive Chat
Click the floating **Message Square** icon in the bottom-right to open the Rosetta Chat:
- Ask codebase-specific questions (e.g., "Where is the auth logic?").
- The AI uses the Knowledge Graph to provide accurate citations and context.

## ✍️ Team Annotations (Persistent)
Collaborate with your team directly on the diagram:
- **Right-Click** any node to open the context menu.
- Select **"Save Annotation"** to add a persistent note.
- These annotations are stored in the backend SQL database and will be visible to all team members exploring the module.
- Perfect for documenting architectural guardrails or legacy warnings.

## 📉 Regression Mode
Visualize how the codebase has changed over time:
- Toggle **Regression Mode** to see color-coded changes.
- **Green**: Newly added modules/entities.
- **Amber**: Modified architectural blocks.
- **Red** (coming soon): Deleted components.

## 🐚 Using the CLI
Generate architectural documentation directly from your terminal:

```bash
# Generate a standard CODEBASE.md for the current directory
python cli/rosetta.py . --persona architect --verbosity standard
```
The resulting file is saved in `/docs/rosetta/codebase_architect_standard.md`.
