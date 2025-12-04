## Phase 3: AI Mode - Natural Language Task Management

### 1. Phase 3 Overview

- **Goal:** Add "AI Mode" to the todo app where users can interact with their tasks using natural language.
- **Scope:** User provides an API key (OpenAI, Gemini, or Claude), enables AI mode, and can then use natural language to perform all CRUD operations on tasks and projects.

### 2. Technology Stack

#### 2.1 OpenAI Agents SDK

We will use the **OpenAI Agents SDK** (`openai-agents` package) which provides:

| Feature                        | Description                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------- |
| **Agent**                      | Core class to define AI assistant with name, instructions, model, tools      |
| **Runner**                     | Executes agent with user input, handles tool calling loop automatically      |
| **@function_tool**             | Decorator to convert Python functions into tools with auto schema generation |
| **AsyncOpenAI**                | OpenAI-compatible client that works with any provider using base_url         |
| **OpenAIChatCompletionsModel** | Model wrapper for custom providers                                           |
| **RunConfig**                  | Configuration for running agent with custom model/provider                   |

**Installation:**

```bash
uv add openai-agents
```

#### 2.2 Multi-Provider Support using AsyncOpenAI

Instead of LiteLLM, we use **AsyncOpenAI** with custom `base_url` to support multiple providers.

> **Important:** User ko sirf **option select** karna hai (1, 2, ya 3) aur **API key** deni hai. Base URL aur model name **automatically** set ho jate hain!

**Pre-defined Provider Constants (User ko manually dene ki zarurat NAHI):**

```python
# src/ai/providers.py

PROVIDER_CONFIG = {
    "openai": {
        "name": "OpenAI (GPT-4)",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini"
    },
    "gemini": {
        "name": "Google Gemini",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model": "gemini-2.0-flash"
    },
    "claude": {
        "name": "Anthropic Claude",
        "base_url": "https://api.anthropic.com/v1",
        "model": "claude-3-5-sonnet-20240620"
    }
}
```

| Provider            | Base URL (Auto)                                            | Model (Auto)                 |
| ------------------- | ---------------------------------------------------------- | ---------------------------- |
| 1. OpenAI           | `https://api.openai.com/v1`                                | `gpt-4o-mini`                |
| 2. Google Gemini    | `https://generativelanguage.googleapis.com/v1beta/openai/` | `gemini-2.0-flash`           |
| 3. Anthropic Claude | `https://api.anthropic.com/v1`                             | `claude-3-5-sonnet-20240620` |

**Provider Configuration Code (base_url aur model automatically select hote hain):**

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

def get_run_config(provider: str, api_key: str):
    """
    Get RunConfig based on provider choice.
    User sirf provider (openai/gemini/claude) aur api_key deta hai.
    Base URL aur model name PROVIDER_CONFIG se automatic aate hain.
    """
    provider_info = PROVIDER_CONFIG[provider]

    client = AsyncOpenAI(
        api_key=api_key,
        base_url=provider_info["base_url"]  # Automatic!
    )

    model = OpenAIChatCompletionsModel(
        model=provider_info["model"],  # Automatic!
        openai_client=client
    )

    config = RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True
    )

    return config
```

### 3. New Features for Phase 3

#### 3.1 API Key Configuration

**Commands:**

| Command            | Description                            |
| ------------------ | -------------------------------------- |
| `ai config`        | Set new provider and API key           |
| `ai config status` | Show current provider (API key hidden) |
| `ai config change` | Change provider or API key             |
| `ai config remove` | Remove saved API key                   |

**Set API Key (First Time):**

```text
> ai config

Select AI provider:
  1. OpenAI (GPT-4)
  2. Google Gemini
  3. Anthropic Claude

Enter choice (1-3): 2
Enter your Gemini API key: AIza...

[OK] Gemini configured successfully.
```

**Check Current Status:**

```text
> ai config status

Current AI Configuration:
  Provider: Google Gemini
  API Key:  AIza...****  (hidden)
  Status:   ✓ Active
```

**Change Provider or Key:**

```text
> ai config change

Current provider: Google Gemini

What do you want to change?
  1. Change provider (will require new API key)
  2. Update API key only

Enter choice (1-2): 1

Select new AI provider:
  1. OpenAI (GPT-4)
  2. Google Gemini
  3. Anthropic Claude

Enter choice (1-3): 1
Enter your OpenAI API key: sk-...

[OK] Switched to OpenAI successfully.
```

**Remove API Key:**

```text
> ai config remove

Are you sure you want to remove your API key? (y/n): y

[OK] API key removed. AI mode is now disabled.
```

**Error when AI mode used without config:**

```text
> ai

[ERROR] No API key configured. Run 'ai config' to set up.
```

**Storage:** API keys stored in `data/config.json`:

```json
{
  "ai_provider": "gemini",
  "api_key": "AIza..."
}
```

When removed, config.json becomes:

```json
{
  "ai_provider": null,
  "api_key": null
}
```

#### 3.2 AI Mode Command

New command to enter AI mode:

```text
> ai
🤖 AI Mode activated. Type your requests in natural language.
   Type 'exit' to return to normal mode.

AI> Show me all my tasks for today

📋 Here are your tasks due today:

ID  Title           Status      Project
--  --------------  ----------  --------
3   Team meeting    [ ] Pending work
7   Buy groceries   [ ] Pending personal

You have 2 tasks due today. Would you like me to help you with any of them?

AI> Create a new project called "fitness" for my workout tasks

[OK] Project 'fitness' created with ID: 4

AI> Add a task "Morning run" to the fitness project, due tomorrow

[OK] Task 'Morning run' created with ID: 12 in project 'fitness', due 2025-12-05

AI> Show me stats

📊 Your Task Statistics:
- Total tasks: 15
- Pending: 8 (53%)
- Completed: 7 (47%)
- Due today: 2
- Overdue: 1

AI> Mark task 3 as complete

[OK] Task 3 'Team meeting' marked as completed.

AI> exit

👋 Exiting AI mode. Back to normal commands.
>
```

#### 3.3 Tool Functions

We will create function tools for all todo operations:

```python
from agents import Agent, Runner, function_tool

# Task Tools
@function_tool
def list_all_tasks() -> str:
    """List all tasks in the todo app."""
    ...

@function_tool
def list_tasks_today() -> str:
    """List all tasks due today."""
    ...

@function_tool
def list_tasks_by_project(project_name: str) -> str:
    """List all tasks in a specific project.

    Args:
        project_name: Name of the project to filter by.
    """
    ...

@function_tool
def add_task(title: str, description: str = "", due_date: str = "", project_name: str = "") -> str:
    """Create a new task.

    Args:
        title: The title of the task (required).
        description: Optional description of the task.
        due_date: Optional due date in YYYY-MM-DD format.
        project_name: Optional project to assign the task to.
    """
    ...

@function_tool
def complete_task(task_id: int) -> str:
    """Mark a task as completed.

    Args:
        task_id: The ID of the task to complete.
    """
    ...

@function_tool
def delete_task(task_id: int) -> str:
    """Delete a task.

    Args:
        task_id: The ID of the task to delete.
    """
    ...

@function_tool
def update_task(task_id: int, title: str = None, description: str = None, due_date: str = None) -> str:
    """Update an existing task.

    Args:
        task_id: The ID of the task to update.
        title: New title (optional).
        description: New description (optional).
        due_date: New due date in YYYY-MM-DD format (optional).
    """
    ...

# Project Tools
@function_tool
def create_project(name: str, description: str = "") -> str:
    """Create a new project.

    Args:
        name: Name of the project.
        description: Optional description.
    """
    ...

@function_tool
def list_projects() -> str:
    """List all projects with task counts."""
    ...

@function_tool
def delete_project(name: str) -> str:
    """Delete a project and all its tasks.

    Args:
        name: Name of the project to delete.
    """
    ...

# Stats Tool
@function_tool
def get_task_stats() -> str:
    """Get statistics about tasks (total, pending, completed, due today, overdue)."""
    ...
```

#### 3.4 Agent Configuration with AsyncOpenAI

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
import json

def load_config():
    """Load AI configuration from config.json"""
    with open("data/config.json") as f:
        return json.load(f)

def get_run_config():
    """Get RunConfig based on user's provider choice."""
    config = load_config()
    provider = config["ai_provider"]
    api_key = config["api_key"]

    if provider == "openai":
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.openai.com/v1"
        )
        model = OpenAIChatCompletionsModel(
            model="gpt-4o-mini",
            openai_client=client
        )
    elif provider == "gemini":
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        model = OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=client
        )
    elif provider == "claude":
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.anthropic.com/v1"
        )
        model = OpenAIChatCompletionsModel(
            model="claude-3-5-sonnet-20240620",
            openai_client=client
        )

    return RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True
    )

# Create Agent with tools
agent = Agent(
    name="Todo Assistant",
    instructions="""You are a helpful todo list assistant.
Help users manage their tasks and projects using natural language.

**IMPORTANT RULES:**

1. **Ask for missing required information:**
   - If user says "create a project" but doesn't give a name, ASK: "What would you like to name the project?"
   - If user says "add a task" but doesn't give a title, ASK: "What's the title of the task?"
   - If user says "delete task" but doesn't give ID, ASK: "Which task would you like to delete? (Give me the task ID)"
   - If user says "mark complete" but doesn't give ID, ASK: "Which task should I mark as complete?"

2. **Use tools appropriately:**
   - When users ask about tasks, use the available tools to fetch and display information.
   - When users want to create, update, or delete tasks/projects, use the appropriate tools.
   - Only call a tool when you have ALL required parameters.

3. **Be conversational:**
   - Always confirm actions after completing them.
   - Provide helpful summaries.
   - If something fails, explain what went wrong.

4. **Handle ambiguity:**
   - If user's request is unclear, ask for clarification.
   - Suggest options when helpful (e.g., "Did you mean the 'work' project or 'personal'?")
""",
    tools=[
        list_all_tasks,
        list_tasks_today,
        list_tasks_by_project,
        add_task,
        complete_task,
        delete_task,
        update_task,
        create_project,
        list_projects,
        delete_project,
        get_task_stats,
    ]
)

# Run AI mode with STREAMING
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import ItemHelpers

async def ai_mode():
    """
    AI Mode with STREAMING support.
    - User dekh sakta hai response real-time generate hote hue
    - User dekh sakta hai konsa tool call ho raha hai
    """
    run_config = get_run_config()
    print("🤖 AI Mode activated (Streaming Enabled)")
    print("   Type 'exit' to return to normal mode.\n")

    while True:
        user_input = input("AI> ").strip()
        if user_input.lower() == "exit":
            print("👋 Exiting AI mode.")
            break

        # Use run_streamed instead of run_sync for streaming
        result = Runner.run_streamed(agent, input=user_input, run_config=run_config)

        async for event in result.stream_events():

            # Show text as it's generated (token by token)
            if event.type == "raw_response_event":
                if isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)

            # Show tool calls and their results
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    print(f"\n🔧 Calling tool: {event.item.name}...")
                elif event.item.type == "tool_call_output_item":
                    print(f"   ✓ Tool output: {event.item.output[:100]}...")  # First 100 chars
                elif event.item.type == "message_output_item":
                    # Final message already streamed above
                    pass

        print()  # New line after response

# Entry point
def start_ai_mode():
    asyncio.run(ai_mode())
```

#### 3.5 Streaming Feature Details

**What User Sees:**

```text
> ai
🤖 AI Mode activated (Streaming Enabled)
   Type 'exit' to return to normal mode.

AI> Show me all tasks for today

🔧 Calling tool: list_tasks_today...
   ✓ Tool output: [{"id": 3, "title": "Team meeting"...

📋 Here are your tasks due today:    <-- Text streams token by token

ID  Title           Status      Project
--  --------------  ----------  --------
3   Team meeting    [ ] Pending work
7   Buy groceries   [ ] Pending personal

AI> Create a project called fitness

🔧 Calling tool: create_project...
   ✓ Tool output: Project 'fitness' created with ID: 4

[OK] I've created the 'fitness' project for you! 🎉

AI> exit
👋 Exiting AI mode.
```

**Streaming Event Types:**

| Event Type                            | Purpose              | User Sees               |
| ------------------------------------- | -------------------- | ----------------------- |
| `raw_response_event`                  | Text being generated | Response token by token |
| `run_item_stream_event` (tool_call)   | Tool is being called | `🔧 Calling tool: X...` |
| `run_item_stream_event` (tool_output) | Tool finished        | `✓ Tool output: ...`    |

**Key Imports for Streaming:**

```python
from agents import Agent, Runner, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
```

### 4. Directory Structure (Phase 3 additions)

```
console-todo-app/
├── src/
│   ├── ai/                      # NEW: AI Mode module
│   │   ├── __init__.py
│   │   ├── agent.py             # Agent configuration with AsyncOpenAI
│   │   ├── tools.py             # Function tools for all operations
│   │   ├── config.py            # API key management
│   │   └── providers.py         # Multi-provider setup (OpenAI, Gemini, Claude)
│   └── ...
├── data/
│   ├── todo.db
│   └── config.json              # NEW: AI configuration (provider, API key)
├── Specification-phase-3/       # NEW: Phase 3 specs
│   └── Specification3.md
└── ...
```

### 5. CLI Additions / Changes

**New Commands:**

| Command     | Description                                    |
| ----------- | ---------------------------------------------- |
| `ai config` | Configure AI provider and API key              |
| `ai`        | Enter AI mode for natural language interaction |

**Updated help output:**

```text
> help

Available commands:
  ...existing commands...

  ai config           - Configure AI provider and API key
  ai                  - Enter AI mode (natural language)
```

### 6. Development Plan for Phase 3 (High Level)

1. **Install dependencies**

   - Add `openai-agents` to project (no litellm needed)

2. **Create AI module structure**

   - Create `src/ai/` directory with submodules

3. **Implement API key configuration**

   - Create `config.py` for storing/loading API keys
   - Implement `ai config` command

4. **Create function tools**

   - Wrap existing TodoManager/ProjectManager methods as `@function_tool`
   - Ensure proper docstrings for auto-schema generation

5. **Configure agent with AsyncOpenAI**

   - Create AsyncOpenAI client with provider-specific base_url
   - Create OpenAIChatCompletionsModel with correct model name
   - Create RunConfig with model, provider, tracing_disabled

6. **Implement AI mode loop**

   - Create interactive AI mode with Runner.run_sync
   - Handle user input/output formatting

7. **Testing**

   - Test with each provider (OpenAI, Gemini, Claude)
   - Test all tool functions

8. **Documentation**
   - Update README with AI mode instructions
   - Document supported providers and setup

### 7. Example Natural Language Queries

The AI assistant should understand and handle queries like:

| User Query                           | Expected Action                                                           |
| ------------------------------------ | ------------------------------------------------------------------------- |
| "Show all tasks"                     | Call `list_all_tasks()`                                                   |
| "What's due today?"                  | Call `list_tasks_today()`                                                 |
| "Show work project tasks"            | Call `list_tasks_by_project("work")`                                      |
| "Add task: Buy milk"                 | Call `add_task("Buy milk")`                                               |
| "Create fitness project"             | Call `create_project("fitness")`                                          |
| "Mark task 5 done"                   | Call `complete_task(5)`                                                   |
| "Delete task 3"                      | Call `delete_task(3)`                                                     |
| "How am I doing?"                    | Call `get_task_stats()`                                                   |
| "Add workout to fitness, due Friday" | Call `add_task("workout", project_name="fitness", due_date="2025-12-06")` |

### 8. Key Imports Summary

```python
from agents import (
    Agent,           # Define AI agent
    Runner,          # Run agent with input
    AsyncOpenAI,     # OpenAI-compatible async client
    OpenAIChatCompletionsModel,  # Model wrapper
    function_tool,   # Decorator for tools
)
from agents.run import RunConfig  # Configuration for running
```
