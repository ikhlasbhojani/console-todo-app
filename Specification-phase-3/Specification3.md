## Spec-Kit Plus – Phase 3 Slash Commands for This Todo App

This file defines the **4 slash commands** for Phase 3 (AI Mode):

> **Note:** `/sp.constitution` was already run in Phase 1.

- `/sp.specify`
- `/sp.plan`
- `/sp.tasks`
- `/sp.implement`

---

### 1. `/sp.specify`

#### 📝 AI Prompt Instruction

```
/sp.specify Create the functional specification for "TODO APP - PHASE 3 (AI Mode)" adding natural language task management.

**PHASE 3 OBJECTIVE:**
Add AI Mode to the todo app where users can interact with tasks and projects using natural language. Support multiple AI providers (OpenAI, Gemini, Claude) using AsyncOpenAI with custom base_url.

**NEW FEATURES:**

### Feature 3.1: API Key Configuration

```

> ai config
> Select AI provider:

1. OpenAI (GPT-4)
2. Google Gemini
3. Anthropic Claude

Enter choice (1-3): 2
Enter your Gemini API key: AIza...

[OK] Gemini API key configured successfully.

```

**Storage:** `data/config.json` stores provider and API key.

### Feature 3.2: AI Mode Interactive Loop

```

> ai
> 🤖 AI Mode activated. Type your requests in natural language.
> Type 'exit' to return to normal mode.

AI> Show me all tasks due today

📋 Tasks due today (2025-12-04):

ID Title Status Project

---

3 Team meeting [ ] Pending work
7 Buy groceries [ ] Pending personal

AI> Create a project called "fitness"

[OK] Project 'fitness' created.

AI> Add task "Morning run" to fitness, due tomorrow

[OK] Task 'Morning run' created in project 'fitness', due 2025-12-05.

AI> Mark task 3 as complete

[OK] Task 3 'Team meeting' marked as completed.

AI> Show stats

📊 Task Statistics:

- Total: 15
- Pending: 8
- Completed: 7
- Due today: 2
- Overdue: 1

AI> exit

👋 Exiting AI mode.

>

```

### Feature 3.3: Natural Language Queries

The AI should understand:
- "Show all tasks" → list_all_tasks()
- "What's due today?" → list_tasks_today()
- "Show work tasks" → list_tasks_by_project("work")
- "Add task: Buy milk" → add_task("Buy milk")
- "Create fitness project" → create_project("fitness")
- "Mark task 5 done" → complete_task(5)
- "Delete task 3" → delete_task(3)

**UPDATED HELP OUTPUT:**
```

> help

Available commands:
...existing Phase 1 & 2 commands...

ai config - Configure AI provider (OpenAI/Gemini/Claude)
ai - Enter AI mode for natural language

```

**VALIDATION RULES:**
- API key must be set before using AI mode
- Invalid API key shows: "[ERROR] Invalid API key. Run 'ai config' to reconfigure."
- AI mode requires internet connection
```

---

### 2. `/sp.plan`

#### 📝 AI Prompt Instruction

````
/sp.plan Create the technical implementation plan for Phase 3 AI Mode using AsyncOpenAI.

**TECHNOLOGY STACK:**
- Python 3.13+
- OpenAI Agents SDK: `openai-agents`

**INSTALLATION:**
```bash
uv add openai-agents
````

**MULTI-PROVIDER SUPPORT using AsyncOpenAI:**

| Provider | Base URL                                                   | Model               |
| -------- | ---------------------------------------------------------- | ------------------- |
| OpenAI   | `https://api.openai.com/v1`                                | `gpt-4o-mini`       |
| Gemini   | `https://generativelanguage.googleapis.com/v1beta/openai/` | `gemini-2.0-flash`  |
| Claude   | `https://api.anthropic.com/v1`                             | `claude-3-5-sonnet` |

**KEY IMPORTS:**

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
```

**PROVIDER CONFIGURATION:**

```python
# Example for Gemini
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)
```

**DIRECTORY STRUCTURE:**

```
src/
├── ai/
│   ├── __init__.py
│   ├── agent.py      # Agent with AsyncOpenAI
│   ├── tools.py      # @function_tool definitions
│   ├── config.py     # API key management
│   └── providers.py  # Provider configs (base_url, model names)
data/
└── config.json       # {"ai_provider": "gemini", "api_key": "..."}
```

**FUNCTION TOOLS (using @function_tool decorator):**

```python
from agents import function_tool

@function_tool
def list_all_tasks() -> str:
    """List all tasks."""

@function_tool
def add_task(title: str, description: str = "", due_date: str = "", project_name: str = "") -> str:
    """Create a new task."""

@function_tool
def complete_task(task_id: int) -> str:
    """Mark task as completed."""

# ... more tools
```

**AGENT + RUNNER with STREAMING:**

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, ItemHelpers

agent = Agent(
    name="Todo Assistant",
    instructions="You are a helpful todo assistant...",
    tools=[list_all_tasks, add_task, complete_task, ...]
)

async def ai_mode():
    # Use run_streamed for streaming
    result = Runner.run_streamed(agent, input=user_input, run_config=config)

    async for event in result.stream_events():
        # Stream text token by token
        if event.type == "raw_response_event":
            if isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

        # Show tool calls
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print(f"🔧 Calling tool: {event.item.name}...")
            elif event.item.type == "tool_call_output_item":
                print(f"✓ Tool output: {event.item.output}")
```

**STREAMING OUTPUT EXAMPLE:**

```text
AI> Show me all tasks for today

🔧 Calling tool: list_tasks_today...
   ✓ Tool output: [{"id": 3, "title": "Team meeting"...

📋 Here are your tasks due today:    <-- Text streams in real-time

ID  Title           Status      Project
--  --------------  ----------  --------
3   Team meeting    [ ] Pending work
```

**API CONFIG COMMANDS:**

| Command            | Description              |
| ------------------ | ------------------------ |
| `ai config`        | Set provider and API key |
| `ai config status` | Show current config      |
| `ai config change` | Change provider/key      |
| `ai config remove` | Remove API key           |

```

---

### 3. `/sp.tasks`

#### 📝 AI Prompt Instruction

```

/sp.tasks

```

> **Note:** This command takes NO arguments.

#### 📋 Expected Output

**PHASE 3.1: DEPENDENCIES**
- Task 1: Add `openai-agents` to pyproject.toml
- Task 2: Run `uv sync` to install dependencies

**PHASE 3.2: AI MODULE STRUCTURE**
- Task 3: Create `src/ai/` directory
- Task 4: Create `src/ai/__init__.py`
- Task 5: Create `src/ai/config.py` for API key management
- Task 6: Create `src/ai/providers.py` with base URLs and model names
- Task 7: Create `data/config.json` schema

**PHASE 3.3: FUNCTION TOOLS**
- Task 8: Create `src/ai/tools.py`
- Task 9: Implement `list_all_tasks()` tool
- Task 10: Implement `list_tasks_today()` tool
- Task 11: Implement `list_tasks_by_project()` tool
- Task 12: Implement `add_task()` tool
- Task 13: Implement `complete_task()` tool
- Task 14: Implement `delete_task()` tool
- Task 15: Implement `update_task()` tool
- Task 16: Implement `create_project()` tool
- Task 17: Implement `list_projects()` tool
- Task 18: Implement `delete_project()` tool
- Task 19: Implement `get_task_stats()` tool

**PHASE 3.4: AGENT SETUP WITH AsyncOpenAI**
- Task 20: Create `src/ai/agent.py`
- Task 21: Implement `get_run_config()` with AsyncOpenAI + OpenAIChatCompletionsModel
- Task 22: Create Agent with instructions and tools
- Task 23: Implement `ai_mode()` function with Runner.run_sync

**PHASE 3.5: CLI COMMANDS**
- Task 24: Implement `ai config` command in main.py
- Task 25: Implement `ai` command to enter AI mode
- Task 26: Update help command

**PHASE 3.6: TESTING**
- Task 27: Test API key configuration
- Task 28: Test each function tool
- Task 29: Test AI mode with each provider

**PHASE 3.7: DOCUMENTATION**
- Task 30: Update README.md with AI mode instructions

---

### 4. `/sp.implement`

#### 📝 AI Prompt Instruction

```

/sp.implement

````

> **Note:** This command takes NO arguments.

#### 📋 Implementation Order

1. Phase 3.1 (Tasks 1-2): Install dependencies
2. Phase 3.2 (Tasks 3-7): Create AI module structure
3. Phase 3.3 (Tasks 8-19): Implement function tools
4. Phase 3.4 (Tasks 20-23): Configure agent with AsyncOpenAI
5. Phase 3.5 (Tasks 24-26): CLI commands
6. Phase 3.6 (Tasks 27-29): Testing
7. Phase 3.7 (Task 30): Documentation

#### 📋 Key Implementation Rules

- Use `AsyncOpenAI` with provider-specific `base_url`
- Use `OpenAIChatCompletionsModel` for model wrapper
- Use `RunConfig` with `tracing_disabled=True` for non-OpenAI
- Use `@function_tool` decorator for all tools
- Store API keys in `data/config.json`

#### 📋 Console Output Format

| Action | Output |
|--------|--------|
| AI mode start | `🤖 AI Mode activated.` |
| AI mode exit | `👋 Exiting AI mode.` |
| Config success | `[OK] <Provider> API key configured.` |
| Config error | `[ERROR] Invalid API key.` |
| No API key | `[ERROR] No API key configured. Run 'ai config'.` |

#### 📋 Run Commands

```bash
# Install dependencies
uv add openai-agents

# Run the app
uv run python -m src.main

# Test AI mode
> ai config
> ai
````

---

## Summary

| Command         | Key Details                                          |
| --------------- | ---------------------------------------------------- |
| `/sp.specify`   | AI mode, API key config, natural language queries    |
| `/sp.plan`      | AsyncOpenAI + OpenAIChatCompletionsModel + RunConfig |
| `/sp.tasks`     | 30 tasks across 7 phases                             |
| `/sp.implement` | Implementation order, output format                  |
