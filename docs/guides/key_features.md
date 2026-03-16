# Key Features of Repo Rosetta

Master the intelligence and navigation features of Repo Rosetta to get the most out of your codebase analysis.

## 🎭 Using Personas
Repo Rosetta's AI can shift its perspective to match your needs. Use the **Persona Selector** in the Explanation Panel:

- **Beginner**: Best for high-level introductions. Uses simple language and analogies.
- **Senior Engineer**: The default mode. Provides technical depth, implementation details, and pattern identification.
- **Architect**: Focuses on the "Big Picture": dependencies, modularity, and large-scale data flow.
- **Product Manager**: Translates code into capabilities and business impact summaries.

## 📏 Adjusting Verbosity
Control the detail of the explanations using the **Verbosity Slider**:

1. **Scan**: A one-line summary. Perfect for rapid browsing of many modules.
2. **Brief**: Highlights the 2-3 most important responsibilities of the code.
3. **Standard**: Detailed overview of internal logic and direct dependencies.
4. **Deep**: Exhaustive analysis, including edge cases and line-by-line mechanics.

## 🗺 Interactive Maps
The **Architecture Map** is the heart of Repo Rosetta:

- **Navigation**: Click and drag to pan, use the scroll wheel to zoom.
- **Selection**: Click on a node to focus the **Explanation Panel** on that specific entity.
- **Hierarchy**: Use the **Layout Toggle** to switch between "Logical/Folder" views and "Dependency" views.
- **MiniMap**: Use the bottom-right MiniMap to navigate large-scale codebases without losing context.

## 💬 Interactive Chat
Click the floating **Message Square** icon in the bottom-right to open the Rosetta Chat:
- Ask codebase-specific questions (e.g., "Where is the auth logic?").
- The AI uses the Knowledge Graph to provide accurate citations and context.

## ✍️ Team Annotations
Collaborate with your team directly on the diagram:
- **Right-Click** any node to add a persistent "Team Note".
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
