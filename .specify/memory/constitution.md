<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 1.0.1 (PATCH - database path clarification)
Modified principles:
  - IV. Database and Persistence: Updated path from `data/todo.db` to `~/.todo-app/todo.db`
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ (no changes needed - Constitution Check section compatible)
  - .specify/templates/spec-template.md ✅ (no changes needed - User scenarios align with testing rules)
  - .specify/templates/tasks-template.md ✅ (no changes needed - Task structure compatible)
Follow-up TODOs: None
==================
-->

# Console Todo Application Constitution

## Core Principles

### I. Code Quality

All code in this project MUST adhere to the following quality standards:

- **Clean, readable code**: Write Python code with meaningful variable and function names that clearly express intent
- **Explicit type hints**: Use Python 3.13+ style type hints for ALL functions, methods, and variables without exception
- **Single responsibility**: Keep functions small and focused on one task (maximum 20-30 lines per function)
- **PEP 8 compliance**: Follow PEP 8 style guidelines, enforced by `ruff` linter
- **Dataclasses for models**: Use `@dataclass` decorator for all data models instead of plain dictionaries
- **Explicit imports**: Prefer explicit imports over wildcard imports (`from module import *` is prohibited)

**Rationale**: Clean, type-safe code reduces bugs, improves maintainability, and enables better tooling support.

### II. Testing

Testing is fundamental to code quality and reliability:

- **Test-driven development**: Prefer writing or designing tests before or alongside code implementation
- **Mandatory test coverage**: Every new feature or bugfix MUST have at least basic `pytest` automated tests
- **No failing tests**: Never leave failing tests in the codebase; fix tests before adding new features
- **pytest framework**: Use `pytest` as the exclusive testing framework with fixtures for database setup/teardown
- **Edge case coverage**: Tests MUST cover edge cases including empty inputs, invalid IDs, and already-completed tasks

**Rationale**: TDD ensures code correctness and prevents regressions while providing living documentation.

### III. Spec-Driven Development

All development MUST follow the Spec-Driven Development methodology:

- **Specs before code**: Specifications in `specs/` folder MUST be written or updated BEFORE major code changes
- **Implementation follows spec**: Code MUST implement the written specification exactly; if behavior needs to change, update the spec first
- **CLI behavior matching**: All CLI behaviors MUST match the documented console flows exactly as specified
- **Output message consistency**: Console output messages MUST match the spec format (e.g., `[OK] Task created with ID: X`)

**Rationale**: Specs provide a single source of truth, enabling clear communication and preventing scope creep.

### IV. Database and Persistence

Data persistence rules are non-negotiable:

- **SQLite persistence**: All data MUST persist in SQLite database at `~/.todo-app/todo.db`
- **No in-memory only**: Never use in-memory only storage; always write to disk for data that should persist
- **Standard library only**: Use Python's built-in `sqlite3` module exclusively (no ORMs like SQLAlchemy)
- **Directory creation**: Create database directory programmatically if it doesn't exist before database operations
- **SQL injection prevention**: Use parameterized queries for ALL database operations to prevent SQL injection

**Rationale**: Consistent persistence ensures data integrity and keeps the application simple and portable.

### V. File and Directory Structure

Project organization MUST follow this structure:

- **Source code**: `src/` directory for all Python source files
- **Tests**: `tests/` directory for all test files
- **Specifications**: `specs/` directory for feature specifications
- **Scripts**: `scripts/` directory for installation and utility scripts
- **User data**: `~/.todo-app/` directory for database and user configuration files

**Rationale**: Consistent structure enables navigation, tooling configuration, and team onboarding.

### VI. Review and Refactor

Code maintenance standards:

- **Regular review**: Regularly review code to simplify and remove dead or duplicate logic
- **Incremental changes**: Prefer small, incremental changes over large, risky edits
- **Pre-commit checks**: Run `ruff check src/` and `ruff format src/` before every commit
- **No commented code**: No commented-out code should remain in production files; delete unused code

**Rationale**: Continuous refactoring prevents technical debt accumulation and maintains code health.

### VII. AI Behavior

Rules governing AI assistant behavior in this project:

- **Protected files**: AI MUST NOT change `constitution.md` or spec files unless the user explicitly requests it
- **Architectural transparency**: AI MUST explain major architectural changes before applying them
- **Package manager compliance**: AI MUST use `uv` for all dependency management operations
- **Workflow compliance**: AI MUST respect the Spec-Driven Development workflow order
- **Agent usage**: AI MUST use the appropriate specialized agent for related work:
  - `python-todo-cli-dev`: Python development (features, models, database, CLI)
  - `todo-testing-agent`: Testing (pytest, CRUD tests, edge cases, persistence)
  - `ai-integration-agent`: AI integration (OpenAI Agents SDK, multi-provider, streaming)
  - `todo-docs-writer`: Documentation (README, specs, docstrings, install scripts)

**Rationale**: Clear AI boundaries ensure predictable behavior and maintain human control over architectural decisions.

## Development Workflow

The standard development workflow for this project:

1. **Specification**: Write or update spec in `specs/` before coding
2. **Planning**: Create implementation plan based on spec
3. **Test Design**: Design test cases covering acceptance criteria
4. **Implementation**: Write code following the spec and constitution rules
5. **Testing**: Run tests to verify implementation
6. **Review**: Run linters, review code, refactor as needed
7. **Documentation**: Update relevant documentation

## Governance

### Amendment Procedure

1. Amendments to this constitution require explicit user approval
2. All changes MUST be documented with rationale
3. Version number MUST be updated following semantic versioning:
   - MAJOR: Backward incompatible changes or principle removals
   - MINOR: New principles or materially expanded guidance
   - PATCH: Clarifications, wording fixes, non-semantic refinements

### Compliance

- This constitution supersedes all other practices when conflicts arise
- All code reviews MUST verify compliance with these principles
- Complexity beyond these rules MUST be explicitly justified

### Guidance File

For runtime development guidance specific to AI assistants, see `CLAUDE.md` in the project root.

**Version**: 1.0.1 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-05
