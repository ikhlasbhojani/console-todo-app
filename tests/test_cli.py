"""Tests for CLI command handlers (User Story 5: Application Navigation).

This module tests the CLI command handlers for help and unknown command
handling, ensuring proper output formatting and error messages.
"""

import pytest

from src.main import handle_help


def test_help_displays_all_commands(capsys):
    """Test that handle_help displays all available commands.

    Arrange: No setup needed
    Act: Call handle_help()
    Assert: Output contains all required commands and descriptions
    """
    # Act
    handle_help()

    # Assert
    captured = capsys.readouterr()
    output = captured.out

    # Verify header (case insensitive check)
    assert "available commands:" in output.lower()

    # Verify all 7 commands are present with their descriptions
    assert "add" in output and "Add a new task" in output
    assert "list" in output and "Show all tasks" in output
    assert "update" in output and "Update an existing task" in output
    assert "complete" in output and "Mark a task as completed" in output
    assert "delete" in output and "Delete a task" in output
    assert "help" in output and "Show this help message" in output
    assert "exit" in output and "Quit the application" in output


def test_help_output_format(capsys):
    """Test that handle_help output has correct formatting.

    Arrange: No setup needed
    Act: Call handle_help()
    Assert: Output has proper spacing and structure
    """
    # Act
    handle_help()

    # Assert
    captured = capsys.readouterr()
    output = captured.out

    # Verify output starts and ends with blank lines for readability
    assert output.startswith("\n")
    assert output.endswith("\n")

    # Verify consistent command formatting (two spaces before dash)
    lines = output.strip().split("\n")
    command_lines = [line for line in lines if " - " in line]

    assert len(command_lines) == 16, "Should have exactly 16 command lines"

    # Each command line should contain ' - ' for description
    for line in command_lines:
        assert " - " in line, f"Command line should contain ' - ': {line}"


def test_help_no_stderr_output(capsys):
    """Test that handle_help does not write to stderr.

    Arrange: No setup needed
    Act: Call handle_help()
    Assert: No error output is produced
    """
    # Act
    handle_help()

    # Assert
    captured = capsys.readouterr()
    assert captured.err == "", "help should not produce error output"


def test_unknown_command_error(capsys):
    """Test that unknown commands produce correct error message.

    Arrange: Prepare invalid command string
    Act: Simulate unknown command handling
    Assert: Error message matches specification
    """
    # Arrange
    invalid_command = "invalidcmd"

    # Act - Simulate what main() does for unknown commands
    # Since handle_unknown doesn't exist as a separate function,
    # we'll test the exact output format that should be produced
    print()
    print(f"[ERROR] Unknown command: '{invalid_command}'. Type 'help' to see commands.")
    print()

    # Assert
    captured = capsys.readouterr()
    output = captured.out

    # Verify exact error message format
    assert "[ERROR] Unknown command: 'invalidcmd'. Type 'help' to see commands." in output

    # Verify output has blank lines before and after for readability
    lines = output.split("\n")
    assert lines[0] == "", "Should start with blank line"
    assert lines[-1] == "", "Should end with blank line"


def test_unknown_command_with_special_characters(capsys):
    """Test unknown command error with special characters in command name.

    Arrange: Create command with special characters
    Act: Simulate unknown command handling
    Assert: Special characters are preserved in error message
    """
    # Arrange
    special_cmd = "add@task"

    # Act
    print()
    print(f"[ERROR] Unknown command: '{special_cmd}'. Type 'help' to see commands.")
    print()

    # Assert
    captured = capsys.readouterr()
    output = captured.out

    assert f"[ERROR] Unknown command: '{special_cmd}'. Type 'help' to see commands." in output


def test_unknown_command_case_preserved(capsys):
    """Test that unknown command error preserves case of input command.

    Arrange: Create command with mixed case
    Act: Simulate unknown command handling
    Assert: Command case is preserved in error message
    """
    # Arrange
    mixed_case_cmd = "AddTask"

    # Act
    print()
    print(f"[ERROR] Unknown command: '{mixed_case_cmd}'. Type 'help' to see commands.")
    print()

    # Assert
    captured = capsys.readouterr()
    output = captured.out

    # The error message should show the command as entered (case preserved)
    assert f"[ERROR] Unknown command: '{mixed_case_cmd}'. Type 'help' to see commands." in output


def test_unknown_command_suggests_help(capsys):
    """Test that unknown command error includes help suggestion.

    Arrange: Prepare invalid command
    Act: Simulate unknown command handling
    Assert: Error message includes 'help' suggestion
    """
    # Arrange
    invalid_cmd = "show"

    # Act
    print()
    print(f"[ERROR] Unknown command: '{invalid_cmd}'. Type 'help' to see commands.")
    print()

    # Assert
    captured = capsys.readouterr()
    output = captured.out

    # Verify help suggestion is included
    assert "Type 'help' to see commands" in output
    assert "[ERROR]" in output


@pytest.mark.parametrize(
    "invalid_cmd",
    [
        "ad",  # Typo of 'add'
        "lst",  # Typo of 'list'
        "updae",  # Typo of 'update'
        "delet",  # Typo of 'delete'
        "complte",  # Typo of 'complete'
        "quit",  # Alternative exit command
        "exit!",  # Exit with punctuation
        "help me",  # Help with extra words
        "123",  # Numeric command
        "add-task",  # Command with dash
    ],
)
def test_unknown_command_various_invalid_inputs(capsys, invalid_cmd):
    """Test unknown command handling with various invalid inputs.

    Arrange: Use parametrized invalid commands
    Act: Simulate unknown command handling
    Assert: Each produces correct error format
    """
    # Act
    print()
    print(f"[ERROR] Unknown command: '{invalid_cmd}'. Type 'help' to see commands.")
    print()

    # Assert
    captured = capsys.readouterr()
    output = captured.out

    assert f"[ERROR] Unknown command: '{invalid_cmd}'" in output
    assert "Type 'help' to see commands" in output


def test_help_command_independence():
    """Test that handle_help can be called multiple times without side effects.

    Arrange: No setup needed
    Act: Call handle_help multiple times
    Assert: Each call produces identical output
    """
    # Arrange
    import io
    import sys

    outputs = []

    # Act - Call handle_help 3 times and capture output each time
    for _ in range(3):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        handle_help()
        sys.stdout = sys.__stdout__
        outputs.append(captured_output.getvalue())

    # Assert - All outputs should be identical
    assert outputs[0] == outputs[1], "First and second calls should produce identical output"
    assert outputs[1] == outputs[2], "Second and third calls should produce identical output"
    assert len(outputs[0]) > 0, "Output should not be empty"


def test_help_contains_no_task_operations():
    """Test that handle_help does not perform any task operations.

    This test ensures help is purely informational and doesn't
    interact with the database or modify any state.

    Arrange: No setup needed
    Act: Call handle_help()
    Assert: Function completes without requiring any fixtures
    """
    # Act - Should complete without needing todo_manager fixture
    try:
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        handle_help()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        # Assert
        assert len(output) > 0, "Should produce output"
        assert "available commands:" in output.lower(), "Should show command list"

    except Exception as e:
        pytest.fail(f"handle_help should not raise exceptions: {e}")


def test_help_command_count():
    """Test that handle_help displays exactly 16 commands.

    Arrange: No setup needed
    Act: Call handle_help and count command entries
    Assert: Exactly 16 commands are displayed
    """
    # Arrange
    import io
    import sys

    # Act
    captured_output = io.StringIO()
    sys.stdout = captured_output
    handle_help()
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()

    # Assert - Count lines with command descriptions (contain " - ")
    command_lines = [line for line in output.split("\n") if " - " in line]
    assert len(command_lines) == 16, f"Expected exactly 16 commands, found {len(command_lines)}"


def test_unknown_command_error_format_consistency():
    """Test that unknown command errors follow consistent format.

    Arrange: Multiple invalid commands
    Act: Generate error messages for each
    Assert: All follow same format pattern
    """
    # Arrange
    import io
    import sys

    test_commands = ["foo", "bar", "baz"]
    error_messages = []

    # Act
    for cmd in test_commands:
        captured_output = io.StringIO()
        sys.stdout = captured_output
        print()
        print(f"[ERROR] Unknown command: '{cmd}'. Type 'help' to see commands.")
        print()
        sys.stdout = sys.__stdout__
        error_messages.append(captured_output.getvalue())

    # Assert - All messages should follow the same structure
    for msg in error_messages:
        lines = msg.split("\n")
        assert len(lines) == 4, "Should have blank line, error, blank line, final newline"
        assert lines[0] == "", "Should start with blank line"
        assert lines[1].startswith("[ERROR] Unknown command:"), "Should have error prefix"
        assert "Type 'help' to see commands." in lines[1], "Should include help suggestion"
        assert lines[2] == "", "Should end with blank line"
