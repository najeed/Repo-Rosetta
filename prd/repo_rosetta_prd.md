# Repo Rosetta Product Requirements Document (PRD)

## 1. Product Overview
Repo Rosetta is an open-source platform that explains the structure, behavior, and purpose of any GitHub repository in a human-readable format. It transforms raw codebases into architecture maps, execution flow diagrams, and contextual explanations accessible to developers of varying expertise levels.

Core value proposition:

"Understand any GitHub repository in 60 seconds."

Repo Rosetta converts repositories into a semantic knowledge graph and uses structured retrieval + LLM reasoning to generate reliable explanations.

---

## 2. Goals

Primary Goals

1. Reduce developer onboarding time for unfamiliar codebases.
2. Make large open-source projects understandable to new contributors.
3. Provide architecture-level visibility into software systems.
4. Enable natural language exploration of repositories.

Secondary Goals

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
Needs:

- Understand architecture quickly
- Find entry points
- Trace execution flows

### 4.2 Engineers onboarding to a new company codebase
Needs:

- System overview
- Module responsibilities
- Data flow understanding

### 4.3 Technical educators and students
Needs:

- Learning explanations
- Simplified code interpretation

### 4.4 Open-source maintainers
Needs:

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
https://Repo Rosetta.dev/org/repo
```

The system displays:

- Repository overview
- Architecture diagrams
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

Output example:

"This repository implements a distributed task queue system for Python applications using Redis as a message broker."

---

### 6.2 Architecture Map

Visual representation of the system structure.

Levels:

- modules
- subsystems
- dependencies

Example:

Client
↓
API Layer
↓
Service Layer
↓
Database

---

### 6.3 Execution Flow Tracing

Trace major workflows through the system.

Example:

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

---

### 6.4 File and Function Explanations

Each file includes:

- purpose
- key functions
- dependencies

Example:

File: auth_service.py

Purpose:
Handles authentication logic including password validation and token generation.

Key functions:
validate_user()
generate_token()

---

### 6.5 Explain Like I'm X

Selectable explanation levels:

- Beginner
- Intermediate
- Senior engineer
- System architect

The explanation depth adapts accordingly.

---

### 6.6 Code Anchor Links

Every explanation references exact code locations.

Example:

validate_user() → auth_service.py#L142

This ensures verifiability.

---

### 6.7 Interactive Repository Q&A

Users can ask questions such as:

- Where is the database connection?
- What is the entry point?
- How does authentication work?

System answers using repository graph traversal.

Conversation context persists during the session.

---

### 6.8 PR / Changelog Explainer

A GitHub bot summarizes pull requests.

Example output:

PR Summary:

Adds Redis caching to reduce database load.

Key Changes:

• Added cache layer
• Modified user_service.get_profile
• Implemented cache invalidation

Impact:
Improves performance for profile lookups.

---

## 7. System Architecture

### 7.1 Repo Ingestion

Responsibilities:

- Clone repository
- Detect languages
- Parse project metadata

Inputs:

GitHub repository URL

---

### 7.2 Code Parsing

Tools:

- tree-sitter
- AST parsing

Extract:

- functions
- classes
- imports
- dependencies

---

### 7.3 Code Knowledge Graph

Graph nodes:

- repository
- module
- file
- class
- function

Edges:

- imports
- calls
- inherits
- defines

This graph becomes the primary retrieval index.

---

### 7.4 Hierarchical Summarization Layer

Generate summaries at multiple levels:

function
↓
file
↓
module
↓
system

Summaries are cached for reuse.

---

### 7.5 Retrieval Engine

Graph traversal retrieves relevant code for queries.

Approach:

Graph + RAG hybrid retrieval.

---

### 7.6 Explanation Engine

LLM generates explanations using:

- retrieved code
- graph metadata
- hierarchical summaries

Focus on correctness and grounded responses.

---

### 7.7 Visualization Engine

Generate:

- dependency graphs
- architecture diagrams
- execution flows

Possible technologies:

- D3.js
- Mermaid

---

## 8. Data Model

Primary entities:

Repository
Module
File
Class
Function
ExecutionFlow
Summary

Relationships capture system structure.

---

## 9. Framework Awareness

Framework detection improves explanation accuracy.

Examples:

FastAPI
Django
React
Spring
Rails

Framework patterns help identify layers such as:

- controllers
- services
- models

---

## 10. Evaluation System

Quality validation dataset containing known repositories.

Example evaluation tasks:

- identify entry point
- identify authentication flow
- locate database configuration

Metrics:

- explanation correctness
- hallucination rate
- anchor accuracy

---

## 11. V1 Scope Priorities

1. URL swap viewer
2. repository architecture map
3. execution flow tracing
4. file and function explanations
5. PR explainer bot

---

## 12. Future Features

### Repo Comparison

Compare architectures of two repositories.

### Onboarding Documentation Export

Generate:

CODEBASE.md

### Repo Signals

Display complexity indicators.

### VSCode Extension

Inline explanations within IDE.

### Interactive Code Map

Zoomable repository exploration.

---

## 13. Distribution Strategy

Primary channels:

- GitHub open-source community
- Hacker News
- developer Twitter
- Reddit programming communities

Demonstrate analysis of well-known repositories.

---

## 14. Success Metrics

Open-source adoption

- GitHub stars
- forks
- contributors

Usage

- repositories analyzed
- Q&A queries

Quality

- explanation accuracy

---

## 15. Long-Term Vision

Repo Rosetta becomes the semantic understanding layer for open-source software.

Future capabilities include:

- architecture discovery
- codebase search
- automated onboarding
- AI-native software documentation

The ultimate goal is to make complex codebases understandable to anyone.

