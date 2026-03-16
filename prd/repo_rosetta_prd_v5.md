# Repo Rosetta Product Requirements Document (PRD)
*Version 5.0*

---

## 1. Product Overview

Repo Rosetta is an open-source platform that explains the structure, behavior, and purpose of any GitHub repository — public or private — in a human-readable format. It transforms raw codebases into architecture maps, execution flow diagrams, and contextual explanations accessible to developers of varying expertise levels.

Private repositories are supported with explicit maintainer authorization. All analysis of private code can be performed either via the hosted web platform (with explicit data handling consent) or entirely locally via the self-hosted CLI, with no code leaving the user's environment.

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

### 4.5 Engineering teams with private codebases
**Needs:**
- Secure, permissioned analysis of internal repositories
- Onboarding documentation for new hires
- Architecture visibility for non-technical stakeholders
- Self-hosted deployment option (no code egress)

### 4.6 CTOs and engineering leaders
**Needs:**
- Architecture-level visibility across multiple internal repos
- Complexity and dependency signals across the codebase
- Onboarding cost reduction

---

## 5. Core Product Experience

### 5.1 Public Repository — URL Swap Interface

User replaces GitHub URL:

```
https://github.com/org/repo
```

with:

```
https://reporosetta.dev/org/repo
```

No login required. The system immediately displays:

- Repository overview
- Interactive architecture diagrams
- Execution flows
- File explanations
- Interactive Q&A

---

### 5.2 Private Repository — Authorized Access Flow

Private repos require explicit maintainer authorization before any analysis occurs.

**Access flow:**

```
1. User visits reporosetta.dev/org/private-repo
        ↓
2. System detects repo is private
        ↓
3. User prompted: "Authorize with GitHub"
        ↓
4. GitHub OAuth — user grants read-only repo scope
        ↓
5. System verifies user has ≥ Maintainer role on that repo
        ↓
6. Analysis proceeds under that authorization
        ↓
7. Output is private to authorized users only
```

**GitHub App alternative (preferred for teams):**
A maintainer installs the Repo Rosetta GitHub App on their organization. This grants scoped read-only access and enables team-wide access without individual OAuth flows per user.

**Self-hosted alternative (for zero-egress requirement):**
Run Repo Rosetta entirely on-premise via CLI. No code ever leaves the organization's environment. See Section 8 for full private repo specification.

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

### 6.5 Persona Selector (Explain Like I'm X)

Controls **vocabulary and assumed knowledge** — not length. The persona setting answers the question: *who is reading this?*

Selectable personas:

| Persona | What changes |
|---|---|
| **Beginner** | Concepts defined on first use; no assumed CS background; analogies used freely |
| **Intermediate** | Standard terminology assumed; patterns named but explained briefly |
| **Senior Engineer** | No hand-holding; precise language; implementation tradeoffs surfaced |
| **System Architect** | Focus on interfaces, contracts, and system boundaries; implementation detail de-emphasized |
| **Product Manager** | Behavior and user impact foregrounded; code mechanics minimized |

The persona setting persists across all diagrams, Q&A responses, file explanations, and exported documents for a consistent session experience. It is stored per-user in the web UI and passable as `--persona` in the CLI.

**Important:** Persona is independent of verbosity. A Senior Engineer can request a one-line scan or a deep architectural audit. A Beginner can request a brief summary or a full tutorial walkthrough. See Section 6.6.

---

### 6.6 Verbosity Control

Controls **how much output is produced** — not vocabulary or assumed knowledge. The verbosity setting answers the question: *how much do I want right now?*

#### Verbosity Levels

**1 — Scan**
Absolute minimum. One line per entity. No prose. Optimized for fast orientation and navigation.
- Format: tables and single-line entries only
- Use case: "I just need to find where X is" or "give me the lay of the land in 10 seconds"
- Analogous to: a file tree with one-line comments

**2 — Brief**
Key points only. Short paragraphs of 2–3 sentences maximum. No rationale, no examples.
- Format: short prose blocks, minimal structure
- Use case: "I have 5 minutes, tell me what matters"
- Analogous to: a well-written README

**3 — Standard** *(default)*
Full contextual explanation. Enough to understand purpose, behavior, and dependencies without reading the code.
- Format: structured prose with examples and code anchors
- Use case: onboarding, exploration, reviewing a PR
- Analogous to: good inline documentation

**4 — Deep**
Exhaustive. Includes rationale, design decisions, edge cases, tradeoffs, and cross-references to related components.
- Format: long-form prose; all examples; linked references to related entities
- Use case: architectural review, debugging a subtle issue, writing technical documentation
- Analogous to: an ADR (Architecture Decision Record) or a thorough technical spec

#### Verbosity is a Format Signal, Not Just a Length Signal

Verbosity controls both *how much* is written and *how it is structured*. At lower verbosity, output collapses into denser, more scannable formats. At higher verbosity, structure expands to support deeper reading.

| Verbosity | Prose | Tables | Code examples | Cross-references | Rationale |
|---|---|---|---|---|---|
| Scan | ❌ | ✅ (dense) | ❌ | ❌ | ❌ |
| Brief | ✅ (2–3 sentences) | ✅ | ❌ | ❌ | ❌ |
| Standard | ✅ (full) | ✅ | ✅ | ✅ (links) | partial |
| Deep | ✅ (long-form) | ✅ | ✅ (multiple) | ✅ (full graph) | ✅ |

The verbosity setting persists across all output surfaces and is passable as `--verbosity [scan|brief|standard|deep]` in the CLI and GitHub Action.

---

### 6.7 Persona × Verbosity Output Matrix

The two controls compose. The same underlying knowledge graph is used for all combinations — only the rendering layer changes. Below is a worked example for a single file explanation (`auth_service.py`) across all four verbosity levels at two persona settings.

#### Senior Engineer persona

**Scan:**
```
auth_service.py — JWT auth, password validation. Calls: database.py, jwt_utils.py
```

**Brief:**
```
auth_service.py
Handles login and token generation. validate_user() checks credentials against the
DB; generate_token() issues a signed JWT. Central dependency for all auth flows.
```

**Standard:**
```
auth_service.py
Owns all authentication logic. validate_user() (L142) fetches the user record,
compares bcrypt hashes, and raises AuthError on failure. generate_token() (L198)
produces a signed HS256 JWT with a 24h expiry. Both functions are called by
auth_controller.py and not intended for direct use outside the service layer.
Depends on: database.py, jwt_utils.py, bcrypt (external).
```

**Deep:**
```
auth_service.py
Central authentication service. Two primary responsibilities: credential validation
and token issuance. validate_user() (L142) takes (email, password), fetches the
user record via database.get_user_by_email(), and performs bcrypt comparison.
Raises AuthError with a generic message on any failure — intentionally non-specific
to avoid user enumeration. No rate limiting at this layer; caller (auth_controller)
is responsible.

generate_token() (L198) issues HS256 JWTs with sub=user_id, exp=now+86400, and
iat=now. The signing secret is read from config.SECRET_KEY at call time (not cached)
— relevant if secret rotation is needed. Token payload is intentionally minimal;
any additional claims should be added here, not in the controller.

Design note: stateless auth. No token store or revocation list. Logout is
client-side only. Consider token revocation list if you need server-side invalidation.

Depends on: database.py (get_user_by_email), jwt_utils.py (sign, decode),
bcrypt (external). Called by: auth_controller.py (L34, L89).
```

---

#### Beginner persona

**Scan:**
```
auth_service.py — Handles login. Creates tokens so the app knows who you are.
```

**Brief:**
```
auth_service.py
This file handles logging in. It checks whether your username and password are
correct, and if so, creates a "token" — a kind of digital ID card the app uses
to recognize you on future requests.
```

**Standard:**
```
auth_service.py
This file is responsible for two things: checking if a user's login credentials
are correct, and creating a "JWT token" — a secure digital pass that the app uses
to verify your identity without asking for your password every time.

When you log in, validate_user() looks up your account and checks your password
using a secure hashing method (bcrypt). If everything matches, generate_token()
creates a token that's valid for 24 hours. This token gets sent back to your
browser and is included with future requests so the server knows who you are.
```

**Deep:**
```
auth_service.py
This file is the "bouncer" of the application — it decides who gets in and gives
them a pass.

The first function, validate_user(), handles the "checking credentials" part.
When you type your email and password, it:
  1. Looks up your account in the database
  2. Takes your password and runs it through bcrypt (a special scrambling process)
  3. Compares the scrambled version against what's stored
  
Why scramble instead of storing the actual password? Because if someone stole the
database, they'd only see scrambled gibberish, not real passwords. This is standard
security practice.

The second function, generate_token(), creates a JWT (JSON Web Token) — think of
it as a wristband at a concert. Once you've proven you're on the guest list, you
get a wristband. For the rest of the night, staff just check the wristband instead
of the list. Your wristband expires after 24 hours, at which point you'd need to
log in again.

This file talks to: database.py (to look up your account) and jwt_utils.py
(which knows how to create and sign tokens).
```

---

### 6.8 Code Anchor Links

Every explanation references exact code locations.

**Example:**

```
validate_user() → auth_service.py#L142
```

This ensures verifiability. Anchors open the corresponding GitHub file and line in a new tab.

---

### 6.9 Interactive Repository Q&A

Users can ask:

- "Where is the database connection?"
- "What is the entry point?"
- "How does authentication work?"

The system answers using repository graph traversal. Conversation context persists during the session. All answers include code anchors.

---

### 6.10 PR / Changelog Explainer

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

When any node is clicked in any diagram, a right-side panel opens. Its content and structure respond to both the active **persona** and **verbosity** settings.

The panel at Standard verbosity / Senior Engineer persona:

```
┌────────────────────────────────────────────────┐
│  auth_service.py                               │
│  Service Layer · 312 lines                     │
├────────────────────────────────────────────────┤
│  [Persona: Senior Eng ▾]  [Verbosity: ●●●○ ▾] │
├────────────────────────────────────────────────┤
│  Purpose                                       │
│  Handles user authentication, password         │
│  validation, and JWT token generation.         │
├────────────────────────────────────────────────┤
│  Key Functions                                 │
│  • validate_user() → L142                      │
│  • generate_token() → L198                     │
│  • hash_password() → L67                       │
├────────────────────────────────────────────────┤
│  Dependencies                                  │
│  • database.py                                 │
│  • jwt_utils.py                                │
│  • bcrypt (external)                           │
├────────────────────────────────────────────────┤
│  [View on GitHub]  [Trace flows]               │
└────────────────────────────────────────────────┘
```

At **Scan** verbosity, the panel collapses to a single-line summary and a function table — no prose blocks rendered. At **Deep** verbosity, the panel expands to include design rationale, edge cases, and cross-references to callers and callees.

The persona and verbosity selectors are visible and adjustable directly within the panel — changing either re-renders the panel content immediately without navigating away.

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

---

## 8. Private Repository Support

This section defines the full permission model, data handling rules, deployment modes, and trust architecture for private repository analysis.

---

### 10.1 Authorization Model

Repo Rosetta operates on a **maintainer-grants-access** model. No analysis of a private repository begins without explicit authorization from a user with at minimum Maintainer-level permissions on that repository.

**Two authorization mechanisms are supported:**

#### GitHub OAuth (individual access)
- User authenticates via GitHub OAuth
- Repo Rosetta requests `repo` scope (read-only)
- System verifies the user holds ≥ Maintainer role on the target repository before proceeding
- Access is scoped to that specific repository and that user's session
- Token stored encrypted; never logged

#### GitHub App Installation (team / organization access)
- A maintainer or org admin installs the Repo Rosetta GitHub App
- App is granted read-only access to selected repositories (maintainer chooses which repos)
- All members of the organization can then access analyses for those repos
- Access revocation: uninstalling the App immediately terminates all access
- Preferred mechanism for engineering teams; eliminates per-user OAuth friction

**Permission check matrix:**

| User role on repo | Can trigger analysis | Can view output | Can share output |
|---|---|---|---|
| Owner / Admin | ✅ | ✅ | ✅ |
| Maintainer | ✅ | ✅ | ✅ |
| Write access | ❌ | ✅ (if invited) | ❌ |
| Read access | ❌ | ✅ (if invited) | ❌ |
| No access | ❌ | ❌ | ❌ |

---

### 10.2 Deployment Modes

Private repo support ships across three deployment modes, ordered by trust level:

#### Mode 1: Hosted (reporosetta.dev)
The code is cloned temporarily into Repo Rosetta's secure cloud environment, analyzed, and the knowledge graph + summaries are stored encrypted behind the user's authorization.

**Appropriate for:** Startups and small teams comfortable with SaaS data handling terms.

**Data handling guarantees (hosted mode):**
- Code is cloned into an isolated, ephemeral container
- Raw code files are deleted immediately after the knowledge graph is built
- Only the knowledge graph, summaries, and diagram layouts are persisted
- Persisted data is encrypted at rest (AES-256) and in transit (TLS 1.3)
- No code content is used for LLM training
- Data retention: knowledge graph persists until the user deletes it or revokes access
- Audit log of all access events available to the repo maintainer

#### Mode 2: Self-Hosted (Docker / Kubernetes)
The maintainer runs Repo Rosetta on their own infrastructure. No code or analysis data leaves the organization's environment.

**Appropriate for:** Companies with data residency requirements, regulated industries (finance, healthcare, government), enterprises with strict infosec policies.

**Deployment:**
```bash
docker run reporosetta/server \
  --github-app-id $APP_ID \
  --github-private-key $KEY_PATH \
  --llm anthropic \          # cloud: anthropic | openai | gemini | azure-openai | bedrock
                             # local: ollama
  --llm-api-key $LLM_API_KEY \
  --storage postgres \
  --port 3000
```

For private repos, the `--llm` flag is **required** in self-hosted mode. Omitting it causes the server to refuse analysis of any private repository at startup.

#### Mode 3: CLI (local, zero-server)
Run analysis entirely on a local machine with no server component. Output is written to local files or stdout.

**Appropriate for:** Individual engineers, security-sensitive workflows, offline environments, CI/CD pipelines.

```bash
# Public repo — cloud LLM used automatically, no flag required
rosetta analyze github.com/org/public-repo --output ./docs/rosetta

# Private repo — --llm flag is REQUIRED, or tool halts with prompt
rosetta analyze ./my-private-repo \
  --llm ollama \             # local: no data leaves the machine
  --output ./docs/rosetta

rosetta analyze github.com/org/private-repo \
  --token $GITHUB_TOKEN \
  --llm anthropic \          # cloud: explicit consent to send excerpts to Anthropic
  --llm-api-key $ANTHROPIC_API_KEY \
  --output ./docs/rosetta \
  --format markdown

rosetta analyze github.com/org/private-repo \
  --token $GITHUB_TOKEN \
  --llm gemini \             # cloud: explicit consent to send excerpts to Google
  --llm-api-key $GEMINI_API_KEY \
  --output ./docs/rosetta

# CI/CD: omitting --llm on a private repo is a hard error (no interactive prompt)
rosetta analyze github.com/org/private-repo \
  --token $GITHUB_TOKEN \
  --llm bedrock \            # AWS tenant-isolated
  --verbosity standard \
  --output ./docs/rosetta
```

---

### 10.3 Access Control for Private Outputs

When a private repo is analyzed, the resulting output is access-controlled by default.

**Visibility rules:**

| Output type | Default visibility | Can be made public? |
|---|---|---|
| Web UI (`reporosetta.dev/org/repo`) | Private (auth required) | Yes, by maintainer explicitly |
| `CODEBASE.md` committed to repo | Inherits repo visibility | N/A (GitHub controls this) |
| Exported PNG / SVG diagrams | Local file, user's control | Yes |
| Shared link (generated URL) | Auth-gated | Yes, maintainer can create public share link |
| Self-hosted output | Organization-internal | Org controls |

**Team access (hosted mode):**
A maintainer can invite specific GitHub users to view the private analysis output. Invited users must authenticate via GitHub — anonymous access to private repo outputs is never permitted.

---

### 10.4 Data Handling Commitments

These commitments apply to all private repositories analyzed via the hosted platform and must be published as a clear, versioned Data Processing Agreement (DPA):

1. **No code retention.** Raw source code is deleted immediately after knowledge graph construction. Only the graph, summaries, and layouts are stored.
2. **No training use.** Code or derived summaries from private repositories are never used to train or fine-tune any model.
3. **Encryption at rest and in transit.** AES-256 for stored data; TLS 1.3 for all network communication.
4. **Audit logs.** Every access event (who viewed what, when) is logged and available to the repo maintainer.
5. **Right to delete.** Maintainer can delete all stored analysis data for their repo at any time via the dashboard or API.
6. **Sub-processor transparency.** The list of sub-processors (LLM providers, cloud infrastructure) is published and updated.
7. **Breach notification.** Affected maintainers notified within 72 hours of any confirmed data breach.

---

### 10.5 LLM Provider Policy

#### Public vs. Private Repository Routing

Repo Rosetta enforces different LLM routing rules depending on repository visibility. This is a hard policy, not a soft default.

**Public repositories:**
Code is publicly visible by definition. Cloud LLMs may be used freely. The default provider is selected automatically based on availability and performance. No explicit user permission is required to send code-derived data to a cloud LLM.

**Private repositories:**
Code is confidential. **No data derived from a private repository may be sent to any cloud LLM without explicit, affirmative permission granted at tool run time.** The tool will not silently fall back to a cloud provider if a local provider fails. If no `--llm` flag is provided when analyzing a private repo, the tool halts and prompts:

```
⚠ This repository is private.
Choose an LLM provider:

  [1] Anthropic Claude (cloud) — code excerpts sent to Anthropic API
  [2] OpenAI GPT-4 (cloud)    — code excerpts sent to OpenAI API
  [3] Google Gemini (cloud)   — code excerpts sent to Google API
  [4] Azure OpenAI (cloud)    — data stays within your Azure tenant
  [5] AWS Bedrock (cloud)     — data stays within your AWS account
  [6] Ollama / local model    — no external API calls

Select [1-6] or pass --llm <provider> to skip this prompt.
```

In non-interactive environments (CI/CD), omitting `--llm` on a private repo is a hard error, not a prompt. This forces an explicit decision in every automated pipeline.

---

#### Supported LLM Providers

| Provider | Type | Public repos | Private repos | Notes |
|---|---|---|---|---|
| Anthropic Claude | Cloud | ✅ Default | ✅ With explicit permission | Strong code reasoning; default for hosted platform |
| OpenAI GPT-4o | Cloud | ✅ | ✅ With explicit permission | Strong general-purpose alternative |
| Google Gemini | Cloud | ✅ | ✅ With explicit permission | Long context window; useful for large repos |
| Azure OpenAI | Cloud (tenant-isolated) | ✅ | ✅ With explicit permission | Data residency within user's Azure tenant |
| AWS Bedrock | Cloud (account-isolated) | ✅ | ✅ With explicit permission | Data residency within user's AWS account |
| Ollama (local) | Local | ✅ | ✅ No permission needed | Zero external API calls; quality varies by model size |

**On Google Gemini:** Gemini's long context window (up to 1M tokens) is particularly useful for large repositories where other providers require more aggressive chunking. It is supported as a first-class provider with the same interface as Anthropic and OpenAI. When selected for private repos, code excerpts are sent to the Google AI API under the user's explicit consent.

**On local models (Ollama):** The only provider that requires no explicit permission for private repos, because no data leaves the machine. Explanation quality depends on the model size deployed. Recommended minimum: a 13B parameter code-specialized model (e.g., `codellama:13b`, `deepseek-coder:6.7b`). Not recommended for Deep verbosity on large repos due to context window constraints.

Only the relevant code excerpts and graph metadata extracted for a given query — never the full raw source of the repository — are sent to any LLM provider at any verbosity level.

---

### 10.6 GitHub App Permissions Scope

The Repo Rosetta GitHub App requests the minimum permissions required:

| Permission | Scope | Reason |
|---|---|---|
| Repository contents | Read-only | Clone repo for analysis |
| Metadata | Read-only | Repo name, description, topics |
| Pull requests | Read-only | PR explainer feature |
| Issues | Read-only | Contribution guidance feature |
| Webhooks | Write | Re-analyze on push events |

The App does **not** request write access to repository contents. It can only write via the PR bot comment feature, which requires an additional explicit opt-in.

---

## 9. Output Formats and Delivery Locations

Repo Rosetta produces output in multiple formats and can deliver it to multiple destinations. Format, destination, persona, and verbosity are all independently configurable.

**The output format is not fixed per destination — it is a function of verbosity.** A `CODEBASE.md` generated at Scan verbosity looks structurally different from one generated at Deep verbosity. This section specifies both the format types and how each responds to the verbosity setting.

---

### 9.1 Output Format Types

#### 9.1.1 Interactive Web Dashboard
The primary output for the hosted platform. A fully interactive React application served at `reporosetta.dev/org/repo` (public) or behind auth (private).

**Contains:**
- Repository overview card
- All diagram types (React Flow, Cytoscape, D3)
- File browser with inline explanations
- Execution flow viewer
- Q&A interface
- Persona selector (persistent across session)
- Verbosity selector (persistent across session, adjustable per-panel)

**Verbosity behavior in the web dashboard:**

| Verbosity | Overview card | Diagram node labels | Explanation panel | Q&A responses |
|---|---|---|---|---|
| Scan | 1-sentence headline | Name only | One-liner + function table | Direct answer, no prose |
| Brief | 2–3 sentence summary | Name + layer badge | Short paragraph + key functions | 2–3 sentence answer |
| Standard | Full overview with tech stack | Name + tooltip on hover | Full explanation with examples | Paragraph with anchors |
| Deep | Full overview + design context | Full annotation | Long-form with rationale + cross-refs | Full exploration with linked entities |

**Best for:** Exploring an unfamiliar repo; onboarding; sharing with team.

---

#### 9.1.2 `CODEBASE.md` (Markdown document)
A single Markdown file committed to the repository root (or `/docs/rosetta/`). Designed to be read in GitHub, VS Code, or any Markdown viewer.

The structure and length of `CODEBASE.md` scales with the verbosity setting. The same sections are always present, but their content density varies significantly.

**Scan verbosity (`--verbosity scan`):**
```
CODEBASE.md

# repo-name

Distributed task queue for Python using Redis.

## Modules
| Module | Purpose |
|---|---|
| api/ | HTTP endpoints |
| services/ | Business logic |
| models/ | Data schemas |
| workers/ | Queue consumers |

## Entry point
`app.py`

## Key flows
- Task submission: api/ → services/task.py → redis
- Task execution: worker.py → services/task.py → database

Generated by Repo Rosetta · [commit SHA] · [date]
```

**Standard verbosity (`--verbosity standard`):**
```
CODEBASE.md

# repo-name — Architecture Guide

## Overview
This repository implements a distributed task queue system for Python applications.
It uses Redis as a message broker and supports async task execution with retry logic.

## Architecture
[Mermaid diagram]

## Key Modules
[Table: module, purpose, key files, key functions]

## Execution Flows
[Mermaid sequence diagrams for top 3 flows]

## File Reference
[File list with 2–3 sentence purposes]

## Glossary
[Key concepts defined]

Generated by Repo Rosetta · [commit SHA] · [date]
```

**Deep verbosity (`--verbosity deep`):**
Includes all Standard content plus: design rationale for architectural choices, module dependency analysis, known complexity hotspots, suggested reading order for new contributors, and cross-references between related components.

**Delivery:** Committed to the repo via PR (opt-in) or written to local filesystem via CLI.

---

#### 9.1.3 `/docs/rosetta/` — Full Documentation Site
A directory of generated Markdown files, one per module and one per major execution flow. Suitable for GitHub Pages, Docusaurus, or Notion import.

**Directory structure:**
```
docs/rosetta/
  index.md              ← repo overview
  architecture.md       ← architecture map (Mermaid)
  flows/
    user-login.md
    file-upload.md
    api-request.md
  modules/
    api/README.md
    services/README.md
    models/README.md
  files/
    auth_service.md
    database.md
    ...
  glossary.md
```

**Delivery:** Written to filesystem via CLI or committed via PR.

---

#### 9.1.4 Diagram Exports (PNG / SVG / Mermaid)
Individual diagram files exported from the interactive canvas.

| Format | Use case |
|---|---|
| PNG | Slack, Notion, Confluence, email |
| SVG | Scalable embed in docs or presentations |
| Mermaid `.mmd` | GitHub README embed, static docs |
| JSON (graph data) | External tooling, custom renderers |

**Delivery:** Download button in the web UI; `--format` flag in CLI.

---

#### 9.1.5 GitHub PR Comment (Bot output)
Automatic summary posted as a comment on pull requests.

**Format:**
```markdown
## 🗺 Repo Rosetta — PR Analysis

**Summary:** Adds Redis caching to reduce database load on profile lookups.

**Files changed:** 4 · **Functions affected:** 7

| File | Change |
|---|---|
| `cache_service.py` | New file — Redis cache abstraction layer |
| `user_service.py` | `get_profile()` now checks cache before DB |
| `config.py` | Added `REDIS_URL` config key |
| `tests/test_user.py` | Added cache invalidation test cases |

**Impact:** Profile lookup performance improvement. Cache invalidation handled on user update.

[View full analysis →](reporosetta.dev/org/repo/pull/142)
```

**Delivery:** GitHub App bot comment, triggered on PR open/update.

---

#### 9.1.6 CLI stdout
Plain text or JSON output to terminal. Verbosity is a first-class CLI flag. Used in CI/CD pipelines and scripting.

```bash
# Scan: one-line per file, machine-readable
rosetta analyze ./repo --verbosity scan --format json

# Standard: default prose explanations written to docs/
rosetta analyze ./repo --verbosity standard --output ./docs/rosetta

# Deep: full documentation site
rosetta analyze ./repo \
  --verbosity deep \
  --persona senior-engineer \
  --output ./docs/rosetta \
  --format markdown

# Pipe scan output into other tools
rosetta analyze ./repo --verbosity scan --format json \
  | jq '.files[] | select(.complexity > 50)'
```

The `--verbosity` flag accepts: `scan`, `brief`, `standard` (default), `deep`.

---

### 9.2 Delivery Locations

| Destination | Format(s) supported | Trigger | Auth required |
|---|---|---|---|
| `reporosetta.dev/org/repo` | Interactive web dashboard | URL visit | No (public) / Yes (private) |
| GitHub PR comment | Bot Markdown output | PR open / push | GitHub App install |
| Repo commit (`CODEBASE.md`) | Markdown | Manual or GitHub Action | Write access to repo |
| `/docs/rosetta/` directory | Markdown site | CLI or GitHub Action | Write access to repo |
| Local filesystem | All formats | CLI | GitHub token (private) |
| Notion / Confluence | Markdown (via export) | Manual export | Platform credentials |
| GitHub Pages | Markdown site | GitHub Action | Repo Pages enabled |

---

### 9.3 GitHub Action

A first-party GitHub Action regenerates documentation on push or release.

```yaml
# .github/workflows/rosetta.yml
name: Repo Rosetta Docs

on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  document:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: reporosetta/action@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          output-format: markdown          # or: json, mermaid
          output-path: docs/rosetta        # default: repo root
          persona: intermediate            # or: beginner, senior-engineer, architect, pm
          verbosity: standard              # or: scan, brief, standard, deep
          commit-output: true              # auto-commit generated docs
          llm: anthropic                   # or: openai, gemini, azure-openai, bedrock, ollama
          llm-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          # For private repos: llm is REQUIRED. Omitting it is a hard error.
          # For public repos: llm defaults to anthropic if omitted.
```

**Provider-specific Action examples:**

```yaml
# Private repo using Gemini (long context, useful for large repos)
llm: gemini
llm-api-key: ${{ secrets.GEMINI_API_KEY }}

# Private repo using Azure OpenAI (data stays in Azure tenant)
llm: azure-openai
llm-api-key: ${{ secrets.AZURE_OPENAI_KEY }}
llm-endpoint: ${{ secrets.AZURE_OPENAI_ENDPOINT }}

# Private repo using Ollama (self-hosted runner, zero egress)
llm: ollama
llm-endpoint: http://ollama.internal:11434
llm-model: codellama:13b
```

**On each run:**
1. Re-analyzes changed files (diff-aware — does not re-analyze unchanged modules)
2. Regenerates affected summaries and diagrams
3. Commits updated `CODEBASE.md` and `/docs/rosetta/` as a bot commit
4. Posts a comment on the triggering PR (if applicable)

---

### 9.4 Output Format and Verbosity Decision Guide

**By situation:**

| Situation | Format | Verbosity | Persona |
|---|---|---|---|
| Exploring a public OSS repo quickly | Web dashboard | Scan or Brief | Senior Engineer |
| Onboarding a new engineer (first day) | Web dashboard + `CODEBASE.md` | Standard | Intermediate |
| Onboarding a new engineer (deep study) | `/docs/rosetta/` | Deep | Intermediate or Senior |
| Team documentation (internal wiki) | `/docs/rosetta/` → Notion | Standard | Intermediate |
| Sharing a diagram in Slack | PNG export | N/A | N/A |
| Embedding a diagram in a README | Mermaid export | N/A | N/A |
| CI/CD automated docs on release | GitHub Action → `CODEBASE.md` | Brief or Standard | Intermediate |
| Architectural review with stakeholders | Web dashboard | Deep | Architect or PM |
| Private repo, zero external data transfer | CLI → local filesystem | Any | Any |
| Non-technical stakeholder briefing | Web dashboard or export | Scan | Product Manager |
| Debugging a subtle behavior | Web dashboard Q&A | Deep | Senior Engineer |

**Verbosity quick reference:**

| Verbosity | Token budget | Best for | Output format character |
|---|---|---|---|
| Scan | ~10% of Standard | Fast triage, navigation, machine-readable | Tables only, no prose |
| Brief | ~30% of Standard | 5-minute read, README-level | Short paragraphs, minimal structure |
| Standard | baseline | Onboarding, exploration, PR review | Structured prose with examples |
| Deep | ~300% of Standard | Architecture review, documentation, debugging | Long-form prose, full cross-references |

---

### 10.1 Repo Ingestion

**Responsibilities:**
- Clone repository
- Detect languages and frameworks
- Parse project metadata (package.json, requirements.txt, etc.)

**Input:** GitHub repository URL

---

### 10.2 Code Parsing

**Tools:**
- `tree-sitter` (multi-language AST)
- Static analysis

**Extracts:**
- Functions and methods
- Classes
- Imports and dependencies
- Module structure

---

### 10.3 Code Knowledge Graph

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

### 10.4 Hierarchical Summarization Layer

Generate LLM summaries at each abstraction level:

```
function → file → module → system
```

Summaries are cached per commit SHA. Stale summaries are invalidated on new commits.

This layer feeds both the explanation panels and the node tooltips in all diagrams.

---

### 10.5 Retrieval Engine

Graph traversal retrieves relevant code and summaries for queries.

**Approach:** Graph + RAG hybrid retrieval.

For large repos exceeding context window limits, the graph structure (not raw code) is the primary navigation layer. Raw code is fetched only for the specific nodes needed.

---

### 10.6 Explanation Engine

The LLM generates explanations using a prompt that encodes four inputs:

- Retrieved code and graph metadata
- Hierarchical summaries (function → file → module → system)
- **Active persona** (controls vocabulary, assumed knowledge, and framing)
- **Active verbosity level** (controls output length, structure, and density)

Persona and verbosity are passed as explicit prompt parameters, not left to the model to infer. The rendering layer receives structured output from the LLM and applies format transforms — collapsing prose to tables at Scan, expanding to long-form at Deep — before displaying to the user.

Summaries at each verbosity level are cached independently per entity per commit SHA. A change to a file invalidates its cached summaries at all verbosity levels but does not affect other files.

Focus on correctness and grounded responses. All claims include code anchors.

---

### 10.7 Visualization Engine

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

## 11. Data Model

**Primary entities:**

| Entity | Key Fields |
|---|---|
| `Repository` | url, name, language, framework, commit_sha, **visibility** (public/private), **access_tier** (hosted/self-hosted/cli) |
| `Module` | name, path, summary, layer_classification |
| `File` | path, language, summary, line_count |
| `Class` | name, file_id, summary |
| `Function` | name, file_id, line_start, line_end, summary, calls[] |
| `ExecutionFlow` | name, steps[], entry_point |
| `Summary` | entity_id, level, content, explain_level, cached_at |
| `DiagramLayout` | repo_id, diagram_type, elk_layout_json, cached_at |
| **`RepoAccess`** | **repo_id, github_user_id, role, granted_by, granted_at, revoked_at** |
| **`AuditLog`** | **repo_id, user_id, action, timestamp, ip_address** |
| **`DataProcessingConsent`** | **repo_id, granted_by, granted_at, version, scope** |

Relationships capture full system structure and feed directly into visualization rendering. For private repositories, all entities are scoped behind the `RepoAccess` permission table.

---

## 12. Framework Awareness

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

## 13. Evaluation System

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

## 14. V1 and V2 Scope Priorities

**V1 — Public repositories only:**

| Priority | Feature |
|---|---|
| 1 | URL swap viewer (`reporosetta.dev/org/repo`) |
| 2 | Architecture map (React Flow + ELK) |
| 3 | Execution flow tracing (top 3–5 flows auto-detected) |
| 4 | File and function explanations with code anchors |
| 5 | Dependency graph (Cytoscape for large repos) |
| 6 | PR explainer GitHub bot |
| 7 | `CODEBASE.md` export via CLI |

**V2 — Private repository support:**

| Priority | Feature |
|---|---|
| 1 | GitHub OAuth + Maintainer role verification |
| 2 | GitHub App installation flow |
| 3 | Private web dashboard (auth-gated) |
| 4 | Self-hosted Docker deployment |
| 5 | Data Processing Agreement (DPA) and audit logs |
| 6 | Configurable LLM backend: Gemini, Azure OpenAI, Bedrock, Ollama — with explicit permission gate for private repos |
| 7 | GitHub Action for automated private repo docs |

---

## 15. Future Features

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

## 16. Distribution Strategy

**Primary channels:**
- GitHub open-source community
- Hacker News (demo on well-known repos)
- Developer Twitter / X
- Reddit programming communities

**Launch strategy:**
Demonstrate analysis of 5–10 well-known, well-documented repos (e.g., FastAPI, Redis, Django). Let the output quality speak. Every shared URL (`reporosetta.dev/org/repo`) is a free distribution event.

---

## 17. Success Metrics

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

## 18. Long-Term Vision

Repo Rosetta becomes the semantic understanding layer for open-source software.

Future capabilities:
- Architecture discovery and search across repositories
- Codebase onboarding automation
- AI-native software documentation standard
- Cross-repo dependency intelligence

The ultimate goal: make any codebase understandable to any person, at any level, in under a minute.
