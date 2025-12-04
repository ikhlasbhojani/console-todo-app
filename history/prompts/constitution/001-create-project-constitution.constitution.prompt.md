---
id: 001
title: Create Project Constitution
stage: constitution
date: 2025-12-04
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: development
user: ikhlasbhojani
command: /sp.constitution
labels: ["constitution", "governance", "project-setup", "sdd"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

Create the constitution.md file with project governance rules for a Python console todo application. This document defines rules and regulations ONLY (no tech stack details).

**PROJECT CONTEXT:**
- Building a command-line todo application with SQLite persistence
- Using Python 3.13+ with package manager `uv`
- Following Spec-Driven Development methodology

**GOVERNANCE RULES TO INCLUDE:**

1. **Code Quality Rules:**
   - Always write clean, readable Python code with meaningful variable and function names
   - Always use explicit type hints (Python 3.13+ style) for all functions, methods, and variables
   - Keep functions small and focused on a single responsibility (max 20-30 lines)
   - Follow PEP 8 style guidelines enforced by `ruff` linter
   - Use `dataclasses` for data models instead of plain dictionaries
   - Prefer explicit imports over wildcard imports

2. **Testing Rules:**
   - Prefer test-driven development (write or design tests before/with code)
   - Every new feature or bugfix must have at least basic `pytest` automated tests
   - Never leave failing tests; fix tests before adding new features
   - Use `pytest` as the testing framework with fixtures for database setup/teardown
   - Test edge cases: empty inputs, invalid IDs, already-completed tasks

3. **Spec-Driven Development Rules:**
   - Specs in `specs/` folder must be written or updated BEFORE major code changes
   - Implementation must follow the written spec; if behavior needs to change, update the spec first
   - All CLI behaviors must match the documented console flows exactly
   - Console output messages must match the spec (e.g., "[OK] Task created with ID: X")

4. **Database and Persistence Rules:**
   - All data must persist in SQLite database at `data/todo.db`
   - Never use in-memory only storage; always write to disk
   - Use Python's built-in `sqlite3` module only (no ORMs like SQLAlchemy)
   - Create `data/` directory if it doesn't exist before database operations
   - Use parameterized queries to prevent SQL injection

5. **File and Directory Rules:**
   - Source code goes in `src/` directory
   - Tests go in `tests/` directory
   - Specifications go in `specs/` directory
   - Installation scripts go in `scripts/` directory
   - Database file goes in `data/` directory

6. **Review and Refactor Rules:**
   - Regularly review code to simplify and remove dead/duplicate logic
   - Prefer small, incremental changes over large, risky edits
   - Run `ruff check src/` and `ruff format src/` before every commit
   - No commented-out code should remain in production files

7. **AI Behavior Rules:**
   - AI must not change `constitution.md` or specs unless the user clearly asks for it
   - AI must explain major architectural changes before applying them
   - AI must follow the package manager `uv` for all dependency management
   - AI must respect the Spec-Driven Development workflow order always use this agents Four agents listed with their specific use cases:
    a. python-todo-cli-dev - Python development (features, models, database, CLI)
    b. todo-testing-agent - Testing (pytest, CRUD tests, edge cases, persistence)
    c. ai-integration-agent - AI integration (OpenAI Agents SDK, multi-provider, streaming)
    d. todo-docs-writer - Documentation (README, specs, docstrings, install scripts)

## Response snapshot

Created constitution.md v1.0.0 with 7 core principles:
- I. Code Quality (type hints, PEP 8, dataclasses, single responsibility)
- II. Testing (TDD, pytest, edge cases, mandatory coverage)
- III. Spec-Driven Development (specs before code, CLI matching)
- IV. Database and Persistence (SQLite, parameterized queries, data/ directory)
- V. File and Directory Structure (src/, tests/, specs/, scripts/, data/)
- VI. Review and Refactor (ruff linting, incremental changes, no dead code)
- VII. AI Behavior (protected files, agent usage requirements)

Added Development Workflow section and Governance section with amendment procedures.
All templates verified compatible. No follow-up TODOs.

## Outcome

- Impact: Initial project governance established with 7 principles
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md (created)
- Next prompts: /sp.specify to create feature specifications
- Reflection: Constitution provides clear guardrails for SDD workflow

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
