---
id: 0002
title: Create Phase2 Implementation Plan
stage: plan
date: 2025-12-05
surface: agent
model: claude-opus-4-5-20251101
feature: 004-phase2-advanced-features
branch: 004-phase2-advanced-features
user: ikhlasbhojani
command: /sp.plan
labels: ["plan", "phase2", "due-dates", "projects", "statistics", "database-migration"]
links:
  spec: specs/004-phase2-advanced-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-phase2-advanced-features/plan.md
  - specs/004-phase2-advanced-features/research.md
  - specs/004-phase2-advanced-features/data-model.md
  - specs/004-phase2-advanced-features/contracts/list-filters.md
  - specs/004-phase2-advanced-features/contracts/projects.md
  - specs/004-phase2-advanced-features/contracts/stats.md
  - specs/004-phase2-advanced-features/quickstart.md
tests:
  - null
---

## Prompt

Create comprehensive implementation plan for TODO APP - PHASE 2 (Advanced Features) based on the spec.md. Technical context includes:

**Database Changes:**
- ALTER TABLE tasks ADD COLUMN due_date TEXT
- ALTER TABLE tasks ADD COLUMN project_id INTEGER
- New projects table with id, name, description, created_at
- Migration using check-and-add approach in TodoManager.__init__

**Data Model:**
- Extended Task dataclass with due_date: date | None and project_id: int | None
- New Project dataclass with id, name, description, created_at, and computed task_count

**New Methods:**
- TodoManager: list_tasks_today(), list_tasks_overdue(), list_tasks_upcoming(), get_stats()
- ProjectManager: create_project(), list_projects(), get_project(), delete_project()

**CLI Updates:**
- list --today, --overdue, --upcoming, --project filters
- project create, list, view, delete commands
- stats command
- undo command (optional)
- Updated add prompts for due date and project

## Response snapshot

Created comprehensive implementation plan for Phase 2 with:

**Phase 0 Research (research.md):**
- RQ-001: SQLite ALTER TABLE ADD COLUMN for schema migration
- RQ-002: Check-and-add migration approach using PRAGMA table_info
- RQ-003: ISO 8601 date format (YYYY-MM-DD) for storage
- RQ-004: SQL WHERE clauses with DATE() functions for filters
- RQ-005: Separate projects table with FK design
- RQ-006: Single SQL query with aggregates for statistics
- RQ-007: In-memory single-action undo approach

**Phase 1 Design:**
- data-model.md: Extended Task (due_date, project_id), new Project entity, TaskStats dataclass
- contracts/list-filters.md: --today, --overdue, --upcoming, --project filter contracts
- contracts/projects.md: Full project CRUD contracts (create, list, view, delete)
- contracts/stats.md: Statistics dashboard contract with metrics and contextual messages
- quickstart.md: Testing guide for all new features

**Technical Decisions:**
- Column migration via ALTER TABLE ADD COLUMN
- Date storage as TEXT (YYYY-MM-DD)
- SQL-level filtering with DATE() functions
- Separate projects table with FK
- In-memory undo (single-level, clears on restart)

## Outcome

- Impact: Complete implementation plan enabling Phase 2 development
- Tests: Test strategy defined in quickstart.md with validation checklist
- Files: plan.md, research.md, data-model.md, 3 contracts, quickstart.md
- Next prompts: /sp.tasks to generate actionable task list
- Reflection: Comprehensive plan covers all technical decisions with clear rationale and CLI contracts

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All constitution checks PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
