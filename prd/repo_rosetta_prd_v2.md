# Repo Rosetta Product Requirements Document (PRD)
*Version 2.0*

---

## 1. Product Overview

Repo Rosetta is an open-source platform that explains the structure, behavior, and purpose of any GitHub repository in a human-readable format. It transforms raw codebases into architecture maps, execution flow diagrams, and contextual explanations accessible to developers of varying expertise levels.

Core value proposition:

> **"Understand any GitHub repository in 60 seconds."**

Repo Rosetta converts repositories into a semantic knowledge graph and uses structured retrieval + LLM reasoning to generate reliable, interactively explorable explanations.

---

## 2. Goals

### Primary Goals

1. Reduce developer onboarding time for unfamiliar codebases.
2. Make large open-source projects understandable to new contributors.
3. Provide architecture-level visibility into software systems.
4. Enable natural language exploration of repositories.

### Secondary Goals

1. Provide automated documentation generation.
2. Enable PR and changelog explanation.
3. Support repository comparison and architectural analysis.

---

## 3. Non-Goals

Initial versions will NOT attempt:

- Code editing
- Automated refactoring
- Security auditing
- Full static analysis replacement

Repo Rosetta focuses on **understanding**, not modification.

---

## 4. Target Users

### 4.1 Developers exploring open-source projects
**Needs:**
- Understand architecture quickly
- Find entry points
- Trace execution flows

### 4.2 Engineers onboarding to a new company codebase
**Needs:**
- System overview
- Module responsibilities
- Data flow understanding

### 4.3 Technical educators and students
**Needs:**
- Learning explanations
- Simplified code interpretation

### 4.4 Open-source maintainers
**Needs:**
- Automated documentation
- PR summaries

---

## 5. Core Product Experience

### URL Swap Interface

User replaces GitHub URL:

```
https://github.com/org/repo
```

with:

```
https://reporosetta.dev/org/repo
```

The system displays:

- Repository overview
- Interactive architecture diagrams
- Execution flows
- File explanations
- Interactive Q&A

---

## 6. Key Features (V1)

### 6.1 Repository Overview

Generate a high-level explanation describing:

- Purpose of the project
- Main capabilities
- Intended users
- Core technologies

**Output example:**

> "This repository implements a distributed task queue system for Python applications using Redis as a message broker."

---

### 6.2 Architecture Map

Visual representation of the system structure.

**Levels:**
- Modules
- Subsystems
- Dependencies

**Example:**

```
Client
  ↓
API Layer
  ↓
Service Layer
  ↓
Database
```

See **Section 7 (Visualization System)** for full rendering specifications.

---

### 6.3 Execution Flow Tracing

Trace major workflows through the system.

**Example:**

```
User login flow

POST /login
  ↓
auth_controller.py
  ↓
auth_service.validate_user()
  ↓
database.get_user()
  ↓
jwt.generate_token()
```

Each node in the flow is clickable and opens an inline explanation panel.

---

### 6.4 File and Function Explanations

Each file includes:
- Purpose
- Key functions
- Dependencies

**Example:**

```
File: auth_service.py

Purpose:
Handles authentication logic including password validation and token generation.

Key functions:
  validate_user()     → auth_service.py#L142
  generate_token()    → auth_service.py#L198
```

---

### 6.5 Explain Like I'm X

Selectable explanation levels:

- Beginner
- Intermediate
- Senior Engineer
- System Architect

The explanation depth adapts accordingly. The selected level persists across all diagrams, Q&A responses, and file explanations for a consistent session experience.

---

### 6.6 Code Anchor Links

Every explanation references exact code locations.

**Example:**

```
validate_user() → auth_service.py#L142
```

This ensures verifiability. Anchors open the corresponding GitHub file and line in a new tab.

---

### 6.7 Interactive Repository Q&A

Users can ask:

- "Where is the database connection?"
- "What is the entry point?"
- "How does authentication work?"

The system answers using repository graph traversal. Conversation context persists during the session. All answers include code anchors.

---

### 6.8 PR / Changelog Explainer

A GitHub bot summarizes pull requests.

**Example output:**

```
PR Summary:
Adds Redis caching to reduce database load.

Key Changes:
  • Added cache layer in cache_service.py
  • Modified user_service.get_profile()
  • Implemented cache invalidation logic

Impact:
Improves performance for profile lookups by ~40%.
```

---

## 7. Visualization System

This section defines the full specification for Repo Rosetta's visual layer — the most differentiating part of the product. All diagrams are interactive, zoomable, and linked to source code.

---

### 7.1 Visualization Philosophy

Repo Rosetta diagrams are not static documentation exports. They are **live, navigable interfaces** — closer to a map than a screenshot. Core principles:

- **Every node is clickable.** Clicking any node (file, module, function) opens an explanation panel.
- **Every diagram is zoomable.** Users move from system view → module view → file view → function view.
- **Every element is anchored.** All nodes link to exact GitHub source locations.
- **Context persists.** "Explain like I'm X" level setting applies to the explanation panel that opens on node click.

---

### 7.2 Visualization Library Stack

#### Why Not Mermaid

Mermaid is a text-to-diagram tool optimized for static documentation embeds. Its limitations make it unsuitable as Repo Rosetta's primary rendering engine:

| Limitation | Impact |
|---|---|
| No true interactivity (click, hover, expand) | Cannot support node inspection |
| No force-directed or hierarchical auto-layout for large graphs | Fails on repos with 100+ nodes |
| No zoom / pan canvas | Cannot support "Google Maps" navigation model |
| Fixed visual aesthetics | Looks generic; no design differentiation |
| No real-time graph updates | Cannot re-render on user filtering |

Mermaid is acceptable as a **fallback export format only** (for embedding in GitHub READMEs and Markdown docs where interactivity is impossible).

---

#### Recommended Library Stack

| Layer | Library | Role |
|---|---|---|
| **Primary diagram canvas** | [React Flow](https://reactflow.dev) | Interactive node-edge diagrams for architecture maps and execution flows |
| **Large graph rendering** | [Cytoscape.js](https://cytoscape.org) | Dependency graphs and call graphs with 100–10,000+ nodes |
| **Layout engine** | [ELK.js](https://eclipse.dev/elk/) | Hierarchical, force-directed, and layered auto-layout for both React Flow and Cytoscape |
| **Custom traces & flows** | [D3.js](https://d3js.org) | Bespoke execution flow animations, data-driven rendering |
| **Export / fallback** | [Mermaid](https://mermaid.js.org) | Static diagram export for Markdown, READMEs, and offline docs |

---

#### Library Rationale

**React Flow**
The best-in-class library for interactive node-based diagrams in React applications. Used by Stripe, Vercel, and GitHub Copilot Workspace. Supports custom node types, edge routing, zoom/pan, minimap, and fully custom styling. Ideal for architecture maps and execution flow views where the node count is moderate (< ~500 nodes).

**Cytoscape.js**
Purpose-built for large, complex network graphs — the standard in bioinformatics and network analysis for graphs with thousands of nodes. Handles rendering performance at scale via canvas-based drawing. Used when visualizing full dependency graphs or call graphs for large repos where React Flow would degrade. Supports 20+ layout algorithms natively.

**ELK.js (Eclipse Layout Kernel)**
The most sophisticated open-source graph layout engine available in JavaScript. Produces dramatically better automatic layouts than Dagre (the common React Flow default) for hierarchical and layered graphs. Critical for generating readable architecture maps without manual node positioning. Integrates with both React Flow (`@xyflow/elk`) and Cytoscape.

**D3.js**
Used for custom, data-driven visualizations that don't fit the node-edge model — primarily animated execution flow traces and the interactive repository "heatmap" (see Section 7.4). D3 gives full control over SVG rendering and transitions.

**Mermaid (export only)**
Retained solely for the "Export as Markdown diagram" feature, allowing users to embed a static diagram in GitHub READMEs, Notion pages, or Confluence documents. Never used as the interactive canvas.

---

### 7.3 Diagram Types

#### 7.3.1 Architecture Map

**Purpose:** Top-level system structure. The first view a user sees.

**Library:** React Flow + ELK.js (layered layout)

**Node types:**
- System boundary (repo root)
- Module / package
- File
- External dependency

**Edge types:**
- Import relationship
- Service call
- Inherits from

**Interactions:**
- Click module node → expand into file nodes
- Click file node → open explanation panel (right sidebar)
- Hover node → show tooltip with one-line purpose
- Double-click → zoom into that node's subgraph
- Minimap in corner for orientation

**Visual design:**
- Color-coded by layer (API layer, service layer, data layer, utility)
- Node size proportional to number of connections (centrality)
- Dimming of unrelated nodes on hover

---

#### 7.3.2 Dependency Graph

**Purpose:** Show what imports what. Critical for understanding coupling and blast radius of changes.

**Library:** Cytoscape.js + ELK.js (force-directed or hierarchical)

**Node types:**
- Internal file nodes
- External package nodes (npm / pip / etc.)

**Edge types:**
- Direct import
- Transitive import (shown as dashed)

**Interactions:**
- Click node → highlight all first-degree dependencies
- Toggle: show/hide external packages
- Toggle: show/hide transitive edges
- Filter by module/directory
- "Isolate this file" view: show only this file's direct dependencies

**Visual design:**
- Internal nodes: solid fill, branded color
- External packages: outlined/ghost style
- Highly-connected nodes rendered larger
- Circular dependency edges highlighted in warning color (amber)

---

#### 7.3.3 Call Graph

**Purpose:** Show which functions call which. Enables tracing of behavior without reading code.

**Library:** Cytoscape.js + Dagre layout

**Node types:**
- Function / method
- Class constructor
- External API call

**Edge types:**
- Direct call
- Async call (dashed)
- Conditional call (dotted)

**Interactions:**
- Click function → open function explanation panel
- "Trace from here" → highlight the full call chain downstream
- "Who calls this?" → highlight all upstream callers
- Filter by file or module scope

---

#### 7.3.4 Execution Flow Diagram

**Purpose:** Trace a specific user-facing workflow end-to-end (e.g., "User Login", "File Upload", "API Request").

**Library:** React Flow (vertical layered layout) + D3 for step animations

**Structure:**
- Each node = one function call or system boundary crossing
- Vertical top-to-bottom flow
- Branching shown for conditional paths (if/else, error paths)

**Interactions:**
- Click step → open explanation panel for that function
- "Step through" mode: highlight nodes sequentially with descriptions (walkthrough mode)
- Show/hide error paths toggle
- Collapse repeated sub-flows (e.g., "validate input" called multiple times)

**Key feature — Walkthrough Mode:**
User clicks "Walk me through this flow." Each node highlights one at a time with an explanation panel advancing automatically. This is the "learning mode" equivalent for flows.

---

#### 7.3.5 Module Dependency Matrix

**Purpose:** Show inter-module coupling at a glance. Especially useful for large repos.

**Library:** D3.js (adjacency matrix heatmap)

**Structure:**
- Rows and columns = modules
- Cell color = coupling intensity (number of cross-module calls)
- Diagonal = self (always empty)

**Interactions:**
- Hover cell → show "Module A calls Module B 14 times"
- Click cell → open dependency graph filtered to those two modules
- Sort rows/columns by coupling score

---

#### 7.3.6 Repo Explorer (Zoomable Treemap)

**Purpose:** "Google Maps for the codebase." Navigate from repo root down to individual functions.

**Library:** D3.js (zoomable treemap / sunburst)

**Structure:**
- Tile size = file size (lines of code) or complexity score
- Color = file type or layer classification
- Drill down: repo → directory → file → functions

**Interactions:**
- Click tile → zoom in
- Breadcrumb trail at top ("src / services / auth")
- Click function name → open explanation panel
- Heatmap toggle: color by complexity, recency of change, or test coverage

---

### 7.4 Visualization Rendering Pipeline

```
Repository Knowledge Graph
         ↓
  Layout Computation (ELK.js)
         ↓
  ┌──────────────────────────────┐
  │   Diagram Type Router        │
  │  • ≤500 nodes → React Flow   │
  │  • >500 nodes → Cytoscape    │
  │  • Matrix view → D3          │
  │  • Flow trace → React Flow   │
  └──────────────────────────────┘
         ↓
  Interactive Canvas Render
         ↓
  Node Click → Graph Traversal → LLM Explanation → Panel
         ↓
  Export: PNG / SVG / Mermaid (static)
```

---

### 7.5 Shared Visual Design System

All diagram types share a consistent visual language:

**Color system:**

| Layer | Color |
|---|---|
| Entry points (routes, controllers) | Blue (#3B82F6) |
| Service / business logic layer | Violet (#8B5CF6) |
| Data / persistence layer | Emerald (#10B981) |
| Utility / helpers | Slate (#64748B) |
| External dependencies | Amber (#F59E0B) |
| Error / warning states | Red (#EF4444) |

**Node anatomy:**
- Icon (file type or layer)
- Label (file or function name)
- Badge (number of connections)
- Tooltip on hover (one-line purpose from LLM summary)

**Edge anatomy:**
- Solid line: direct, synchronous relationship
- Dashed line: async or conditional
- Arrow direction: dependency direction
- Edge label (optional): relationship type

**Zoom levels:**
- Level 1 (overview): Module nodes only, no edges within modules
- Level 2 (structure): File nodes visible, module grouping shown
- Level 3 (detail): Function nodes visible within files
- Level 4 (deep): Full call graph within a single file

---

### 7.6 Explanation Panel (Node Click Behavior)

When any node is clicked in any diagram, a right-side panel opens with:

```
┌─────────────────────────────────────┐
│  auth_service.py                    │
│  Service Layer · 312 lines          │
├─────────────────────────────────────┤
│  Purpose                            │
│  Handles user authentication,       │
│  password validation, and JWT       │
│  token generation.                  │
├─────────────────────────────────────┤
│  Key Functions                      │
│  • validate_user() → L142           │
│  • generate_token() → L198          │
│  • hash_password() → L67            │
├─────────────────────────────────────┤
│  Dependencies                       │
│  • database.py                      │
│  • jwt_utils.py                     │
│  • bcrypt (external)                │
├─────────────────────────────────────┤
│  [View on GitHub]  [Trace flows]    │
└─────────────────────────────────────┘
```

- Explanation level respects current "Explain Like I'm X" setting.
- "Trace flows" button activates an execution flow diagram starting from this file.
- All function names are clickable anchors to GitHub source.

---

### 7.7 Export Formats

| Format | Use Case | Library |
|---|---|---|
| PNG / SVG | Sharing in docs, Slack, Notion | React Flow / Cytoscape export API |
| Mermaid (`.mmd`) | GitHub README embeds | Mermaid serializer |
| `CODEBASE.md` | Onboarding documentation | Markdown with embedded Mermaid |
| JSON (graph data) | External tooling, programmatic use | Raw knowledge graph export |

---

## 8. System Architecture

### 8.1 Repo Ingestion

**Responsibilities:**
- Clone repository
- Detect languages and frameworks
- Parse project metadata (package.json, requirements.txt, etc.)

**Input:** GitHub repository URL

---

### 8.2 Code Parsing

**Tools:**
- `tree-sitter` (multi-language AST)
- Static analysis

**Extracts:**
- Functions and methods
- Classes
- Imports and dependencies
- Module structure

---

### 8.3 Code Knowledge Graph

**Graph nodes:**
- Repository
- Module
- File
- Class
- Function

**Edges:**
- `imports`
- `calls`
- `inherits`
- `defines`

This graph is the primary retrieval index and the source of truth for all visualizations.

---

### 8.4 Hierarchical Summarization Layer

Generate LLM summaries at each abstraction level:

```
function → file → module → system
```

Summaries are cached per commit SHA. Stale summaries are invalidated on new commits.

This layer feeds both the explanation panels and the node tooltips in all diagrams.

---

### 8.5 Retrieval Engine

Graph traversal retrieves relevant code and summaries for queries.

**Approach:** Graph + RAG hybrid retrieval.

For large repos exceeding context window limits, the graph structure (not raw code) is the primary navigation layer. Raw code is fetched only for the specific nodes needed.

---

### 8.6 Explanation Engine

LLM generates explanations using:
- Retrieved code
- Graph metadata
- Hierarchical summaries
- Current "Explain Like I'm X" level

Focus on correctness and grounded responses. All claims include code anchors.

---

### 8.7 Visualization Engine

**Responsibilities:**
- Compute graph layouts via ELK.js
- Route diagram type based on node count and diagram class
- Serve interactive diagram data to frontend
- Generate static export formats

**Technologies:**
- React Flow (architecture maps, execution flows)
- Cytoscape.js (large dependency and call graphs)
- D3.js (treemap explorer, matrix view, custom traces)
- ELK.js (layout computation for all diagram types)
- Mermaid (static export only)

See **Section 7** for full specification.

---

## 9. Data Model

**Primary entities:**

| Entity | Key Fields |
|---|---|
| `Repository` | url, name, language, framework, commit_sha |
| `Module` | name, path, summary, layer_classification |
| `File` | path, language, summary, line_count |
| `Class` | name, file_id, summary |
| `Function` | name, file_id, line_start, line_end, summary, calls[] |
| `ExecutionFlow` | name, steps[], entry_point |
| `Summary` | entity_id, level, content, explain_level, cached_at |
| `DiagramLayout` | repo_id, diagram_type, elk_layout_json, cached_at |

Relationships capture full system structure and feed directly into visualization rendering.

---

## 10. Framework Awareness

Framework detection improves explanation accuracy and layer classification for visualizations.

**Detected frameworks:**

| Framework | Layer Heuristics |
|---|---|
| FastAPI / Flask / Django | routes → controllers → services → models |
| React / Next.js | pages → components → hooks → utils |
| Spring Boot | controllers → services → repositories |
| Rails | controllers → models → views |
| Express.js | routes → middleware → controllers |

Framework patterns determine node color assignment by layer in all architecture diagrams.

---

## 11. Evaluation System

Quality validation dataset containing known, well-documented repositories.

**Evaluation tasks:**
- Identify entry point
- Identify authentication flow
- Locate database configuration
- Describe purpose of a given file

**Metrics:**
- Explanation correctness (human eval on sample set)
- Hallucination rate (claim not grounded in source code)
- Anchor accuracy (code link points to correct location)
- Diagram correctness (edges reflect actual import/call relationships)

A passing hallucination rate threshold must be met before any public-facing launch.

---

## 12. V1 Scope Priorities

| Priority | Feature |
|---|---|
| 1 | URL swap viewer (`reporosetta.dev/org/repo`) |
| 2 | Architecture map (React Flow + ELK) |
| 3 | Execution flow tracing (top 3–5 flows auto-detected) |
| 4 | File and function explanations with code anchors |
| 5 | Dependency graph (Cytoscape for large repos) |
| 6 | PR explainer GitHub bot |

---

## 13. Future Features

### Repo Comparison
Compare architectures of two repositories side by side.

### Onboarding Documentation Export
Generate a `CODEBASE.md` or Notion-compatible doc.

### Repo Signals
Display complexity and coupling indicators. Framed as contributor signals, not grades.

### VSCode Extension
Inline explanations within the IDE. Hover any file → architecture panel.

### Repo Explorer (Zoomable Treemap)
Full "Google Maps" experience. Zoom from repo root to individual functions. (Section 7.3.6)

### Module Dependency Matrix
D3 adjacency heatmap showing inter-module coupling at a glance. (Section 7.3.5)

### Diff-Aware Explanations
Re-explain only what changed between two commits. Essential for the GitHub Action use case.

### Embeddable Badge
```
[![Explained on Repo Rosetta](badge)](reporosetta.dev/org/repo)
```
Maintainers add to READMEs voluntarily.

---

## 14. Distribution Strategy

**Primary channels:**
- GitHub open-source community
- Hacker News (demo on well-known repos)
- Developer Twitter / X
- Reddit programming communities

**Launch strategy:**
Demonstrate analysis of 5–10 well-known, well-documented repos (e.g., FastAPI, Redis, Django). Let the output quality speak. Every shared URL (`reporosetta.dev/org/repo`) is a free distribution event.

---

## 15. Success Metrics

### Open-source Adoption
- GitHub stars and forks
- Contributors

### Usage
- Repositories analyzed
- Q&A queries per session
- Diagram interactions (node clicks, zoom events)

### Quality
- Explanation accuracy (eval harness)
- Anchor accuracy rate
- Hallucination rate (must remain below threshold)

---

## 16. Long-Term Vision

Repo Rosetta becomes the semantic understanding layer for open-source software.

Future capabilities:
- Architecture discovery and search across repositories
- Codebase onboarding automation
- AI-native software documentation standard
- Cross-repo dependency intelligence

The ultimate goal: make any codebase understandable to any person, at any level, in under a minute.
