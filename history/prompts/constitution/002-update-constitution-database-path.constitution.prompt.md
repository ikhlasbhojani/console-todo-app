---
id: 0002
title: Update Constitution Database Path
stage: constitution
date: 2025-12-05
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: development
user: ikhlasbhojani
command: /sp.constitution
labels: ["constitution", "governance", "database-path", "patch"]
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
   - AI must respect the Spec-Driven Development workflow order

## Response snapshot

Constitution already exists at version 1.0.0 with all 7 principles. Updated to version 1.0.1 with a PATCH change:

**Version change**: 1.0.0 → 1.0.1 (PATCH)

**Modification**: Updated database path in Principle IV (Database and Persistence) from `data/todo.db` to `~/.todo-app/todo.db` to match the actual implementation.

**Also updated**: Principle V (File and Directory Structure) to reflect user data location at `~/.todo-app/` instead of `data/` directory.

**Template verification**: All templates (plan-template.md, spec-template.md, tasks-template.md) remain compatible with constitution principles.

## Outcome

- Impact: Constitution updated to reflect actual implementation database path
- Tests: N/A (documentation change)
- Files: .specify/memory/constitution.md
- Next prompts: N/A
- Reflection: Constitution should be kept in sync with actual implementation decisions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All template compatibility checks PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
