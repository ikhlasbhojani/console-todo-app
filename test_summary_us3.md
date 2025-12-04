# Test Summary: User Story 3 - Update Task Details

## Overview
Comprehensive test suite for TodoManager.update_task() method following TDD principles.

## Location
- **File**: `/home/ikhlasbhojani/Desktop/hackathon-part-2/console-todo-app/tests/test_todo_manager.py`
- **Test Class**: `TestUpdateTask`
- **Lines**: 499-949

## Tests Added (14 Total)

### Required Tests (4 from Task List)

#### 1. test_update_task_title_only (T039)
- **Purpose**: Verify updating only the title while preserving description
- **Verifies**:
  - Returns True on success
  - Title is updated to new value
  - Description remains unchanged
  - Status remains unchanged
  - updated_at timestamp is modified
  - Database reflects changes

#### 2. test_update_task_description_only (T040)
- **Purpose**: Verify updating only the description while preserving title
- **Verifies**:
  - Returns True on success
  - Description is updated to new value
  - Title remains unchanged
  - Status remains unchanged
  - updated_at timestamp is modified
  - Database reflects changes

#### 3. test_update_task_not_found (T041)
- **Purpose**: Verify behavior when updating non-existent task
- **Verifies**:
  - Returns False for non-existent task ID
  - No errors are raised
  - Database remains unchanged

#### 4. test_update_task_preserves_unchanged_fields (T042)
- **Purpose**: Verify updating with None parameters preserves all fields
- **Verifies**:
  - Returns True if task exists (even with no changes)
  - Title remains unchanged when None is passed
  - Description remains unchanged when None is passed
  - Status remains unchanged

### Extended Tests (10 Additional)

#### 5. test_update_task_both_fields_together
- **Purpose**: Test updating both title and description simultaneously
- **Coverage**: Both parameters modified in single call

#### 6. test_update_task_empty_title_raises_error
- **Purpose**: Verify ValueError is raised for empty title
- **Coverage**: Input validation, error handling

#### 7. test_update_task_whitespace_only_title_raises_error
- **Purpose**: Verify ValueError is raised for whitespace-only title
- **Coverage**: Edge case validation

#### 8. test_update_task_strips_title_whitespace
- **Purpose**: Verify title is trimmed of leading/trailing whitespace
- **Coverage**: Input normalization

#### 9. test_update_task_to_empty_description
- **Purpose**: Verify description can be set to empty string
- **Coverage**: Empty string vs None distinction

#### 10. test_update_task_with_special_characters
- **Purpose**: Test special characters and unicode in updates
- **Coverage**: Character encoding, SQL injection safety

#### 11. test_update_task_persistence_across_restart
- **Purpose**: Verify updates persist after database reconnection
- **Coverage**: SQLite persistence, simulated app restart

#### 12. test_update_task_multiple_updates_sequential
- **Purpose**: Test multiple sequential updates to same task
- **Coverage**: Timestamp progression, state management

#### 13. test_update_task_with_very_long_title
- **Purpose**: Test updating with 500 character title
- **Coverage**: Maximum length inputs, boundary conditions

#### 14. test_update_task_with_newlines_in_description
- **Purpose**: Test multiline descriptions with newlines
- **Coverage**: Special characters, text formatting

## Test Execution Results

### Collection
```bash
uv run pytest tests/test_todo_manager.py::TestUpdateTask --collect-only
```
**Result**: 14 tests collected successfully

### Execution
```bash
uv run pytest tests/test_todo_manager.py -v -k update
```
**Result**: All 14 tests FAILED (as expected - method not implemented yet)

**Error**: `AttributeError: 'TodoManager' object has no attribute 'update_task'`

This is the **expected behavior** in TDD:
1. Write tests first (RED phase)
2. Tests fail because implementation doesn't exist
3. Next step: Implement update_task method (GREEN phase)
4. Tests should pass after implementation

## Contract Compliance

The tests are written to verify compliance with the contract from `specs/001-todo-sqlite/contracts/cli-commands.md`:

```python
def update_task(
    self,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> bool:
    """Update an existing task's title and/or description."""
```

### Contract Requirements Tested:
- [x] Returns bool (True on success, False if not found)
- [x] title=None means keep current value
- [x] description=None means keep current value
- [x] Empty title raises ValueError
- [x] Whitespace-only title raises ValueError
- [x] Title is stripped of whitespace
- [x] updates_at timestamp is modified on success
- [x] Both None parameters still returns True if task exists

## Testing Standards Applied

### AAA Pattern (Arrange-Act-Assert)
All tests follow the AAA pattern with clear sections

### Test Naming Convention
`test_<method>_<scenario>_<expected_outcome>`

### Fixtures Used
- `todo_manager`: TodoManager with temporary database
- `temp_db`: Temporary database path for isolation

### Database Isolation
All tests use temporary databases via `temp_db` fixture to ensure:
- Test independence
- No side effects
- Clean state for each test

### Coverage Areas
1. **Happy Path**: Successful updates
2. **Error Cases**: Not found, validation errors
3. **Edge Cases**: Special characters, long inputs, multiline text
4. **Persistence**: Database persistence across restarts
5. **State Management**: Multiple updates, field preservation

## Next Steps

1. **Implement update_task method** in TodoManager
2. **Run tests again** to verify implementation
3. **Achieve GREEN state** (all tests passing)
4. **Refactor if needed** while keeping tests passing

## File References

### Main Test File
`/home/ikhlasbhojani/Desktop/hackathon-part-2/console-todo-app/tests/test_todo_manager.py`

### Fixtures File
`/home/ikhlasbhojani/Desktop/hackathon-part-2/console-todo-app/tests/conftest.py`

### Implementation Target
`/home/ikhlasbhojani/Desktop/hackathon-part-2/console-todo-app/src/todo_manager.py`
(update_task method needs to be added)

## Test Quality Metrics

- **Total Tests**: 14
- **Required Tests**: 4/4 (100%)
- **Extended Tests**: 10 additional
- **Code Coverage Target**: 80%+ (when implementation complete)
- **Documentation**: All tests have comprehensive docstrings
- **Assertions**: Multiple assertions per test with descriptive messages
- **Test Independence**: All tests are isolated and can run in any order
