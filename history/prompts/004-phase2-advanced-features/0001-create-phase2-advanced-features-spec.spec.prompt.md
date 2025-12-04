---
id: 0001
title: Create Phase2 Advanced Features Spec
stage: spec
date: 2025-12-05
surface: agent
model: claude-opus-4-5-20251101
feature: 004-phase2-advanced-features
branch: 004-phase2-advanced-features
user: ikhlasbhojani
command: /sp.specify
labels: ["spec", "phase2", "due-dates", "projects", "statistics", "undo"]
links:
  spec: specs/004-phase2-advanced-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-phase2-advanced-features/spec.md
  - specs/004-phase2-advanced-features/checklists/requirements.md
tests:
  - null
---

## Prompt

Create the functional specification for "TODO APP - PHASE 2 (Advanced Features)" building on the Phase 1 SQLite todo application.

**PHASE 2 OBJECTIVE:**
Add advanced features to the Phase 1 console todo app: due dates with filtered views, project categorization, statistics, and optional undo functionality.

**NEW DATA MODEL FIELDS:**
- **due_date**: Optional date when task is due (stored as TEXT in ISO format: YYYY-MM-DD)
- **project**: Optional project/category name (e.g., "work", "personal", "study")

**NEW FEATURES:**
- Feature 2.1: Due Dates & Filtered Views (list --today, --overdue, --upcoming)
- Feature 2.2: Project Management (Full CRUD with project create/list/view/delete)
- Feature 2.3: Stats Command (task statistics dashboard)
- Feature 2.4: Undo Command (Optional/Stretch - single-level undo)

## Response snapshot

Created comprehensive specification for TODO APP - PHASE 2 (Advanced Features) with:

**4 User Stories:**
- US1 (P1): Due Dates and Filtered Task Views - assign due dates, filter by today/overdue/upcoming
- US2 (P2): Project Management with Full CRUD - create/list/view/delete projects, assign tasks to projects
- US3 (P3): Task Statistics Dashboard - total/pending/completed counts, due today, overdue, completion rate
- US4 (P4 - Optional): Undo Last Action - single-level undo for add/delete/complete/update

**25 Functional Requirements:**
- FR-001 to FR-007: Due dates and filters
- FR-008 to FR-016: Project management
- FR-017 to FR-020: Statistics
- FR-021 to FR-023: Undo (SHOULD, optional)
- FR-024 to FR-025: Help and UI updates

**8 Success Criteria:**
- Task creation with due dates under 30 seconds
- Filter commands return results under 1 second
- Project operations complete under 2 seconds
- Stats calculation under 1 second for 1000 tasks
- 100% accuracy for filtered views and undo

**Key Entities:**
- Task (extended with due_date and project_id)
- Project (new entity with name, description, created_at)

## Outcome

- Impact: Complete Phase 2 specification enabling advanced task management
- Tests: Acceptance scenarios for all 4 user stories with edge cases
- Files: spec.md, checklists/requirements.md
- Next prompts: /sp.plan to create implementation plan
- Reflection: Comprehensive spec covers all requested features with clear boundaries and optional undo as stretch goal

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All checklist items PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
