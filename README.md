# Build AI Agents in Pure Python

Learn how to build AI agents with the OpenAI API, one step at a time: start with a single API call, add conversation history, introduce a tool, and bring it all together in an interactive coding agent.

The agent logic is written directly in Python using the official OpenAI SDK and Python's standard library. Each example keeps the API requests, messages, tool definitions, and execution loop visible so you can follow how the pieces work together.

## What you'll learn

- Send a request to the OpenAI Chat Completions API and read the response.
- Maintain conversation history across multiple turns.
- Describe Python functions as tools using JSON schemas.
- Execute tool calls locally and send their results back to the model.
- Build an agent loop that continues until the model returns a final response.
- Give a coding agent file access and shell commands with command approval.

Basic familiarity with Python functions, lists, and dictionaries is enough to get started.

## Learning path

Read and run the examples in this order. Each script runs independently; you do not need to leave an earlier step running.

| Stage | File | What it introduces |
| --- | --- | --- |
| 1. Your first API call | [`step1.py`](step1.py) | Sends a fixed prompt asking for a one-sentence explanation of an AI agent and prints the response. |
| 2. A conversational chatbot | [`step2.py`](step2.py) | Adds an interactive terminal loop and stores user and assistant messages in memory. |
| 3. Your first tool | [`step3.py`](step3.py) | Defines a `read_file` tool, asks the model to summarize `example.txt`, executes tool calls, and returns results to the model. |
| 4. An interactive coding agent | [`agent.py`](agent.py) | Combines conversation history, four tools, tool dispatch, and a repeated model–tool loop. |

The examples use `gpt-5-mini` and `client.chat.completions.create()`.

## Getting started

### 1. Get the code

```bash
git clone https://github.com/nepseli/AI_Agent_in_pure_Python.git
cd AI_Agent_in_pure_Python
```

Alternatively, download and extract the repository ZIP, then open a terminal in the extracted project folder.

### 2. Install dependencies

You need **Python 3.13 or later**, an internet connection, and an OpenAI API key with access to the model used by the examples. Running the examples makes API requests and may incur charges.

The repository includes `pyproject.toml` and `uv.lock`. If you use uv:

```bash
uv sync
```

Or create a virtual environment with Python:

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install the SDK dependency declared by the project:

```bash
python -m pip install "openai>=3.7.0"
```

### 3. Configure your API key

**Before running Steps 1–3:** replace the hardcoded `client = OpenAI(api_key=...)` line in each of `step1.py`, `step2.py`, and `step3.py` with:

```python
client = OpenAI()
```

This lets the SDK read `OPENAI_API_KEY` from your environment. `agent.py` already uses this environment variable.

Set your own key in the terminal where you will run the examples.

**macOS/Linux:**

```bash
export OPENAI_API_KEY="your-api-key"
```

**Windows PowerShell:**

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

Do not commit API keys. Revoke any key previously included in source code. The scripts do not automatically load `.env` files; if you add one yourself, also add it to `.gitignore`.

### 4. Run the examples

From the repository root, run one script at a time:

```bash
uv run step1.py
uv run step2.py
uv run step3.py
uv run agent.py
```

If you installed with pip, use `python` instead of `uv run`:

```bash
python step1.py
python step2.py
python step3.py
python agent.py
```

Steps 1 and 3 use fixed prompts and finish after producing a response. Step 2 and `agent.py` are interactive: type `exit` or `quit` to stop.

## Try the coding agent

Start `agent.py`, then enter a task at the `You:` prompt. For example:

```text
List the files in the current directory.
```

```text
Read example.txt and summarize it in one sentence.
```

```text
Create a file called greeting.py that prints a friendly greeting.
```

```text
Run greeting.py and tell me the output.
```

These are suggested prompts; responses and tool choices can vary. The terminal prints tool names and arguments as the agent works, followed by its final reply.

### Available tools

| Tool | Behavior |
| --- | --- |
| `list_files(path)` | Returns the names of entries in a directory. |
| `read_file(path)` | Reads a UTF-8 text file. |
| `write_file(path, content)` | Creates or overwrites a text file. Its parent directory must already exist. |
| `run_command(command)` | Requests approval, then runs a shell command with a 120-second timeout and returns its output. |

For shell commands, enter `y` to approve execution. Any other response declines the command and returns that decision to the model.

**Use a disposable project folder when experimenting.** File writes do not ask for approval and can overwrite existing content. File paths are not restricted to the launch directory, and approved commands run with your user account's permissions. Contents read through tools are sent back to the API as part of the conversation.

## How the agent loop works

The model requests tools; the Python program executes them.

1. The program adds your request to the message history.
2. It sends the history and tool schemas to the model.
3. If the model requests tools, Python parses their arguments and calls the matching functions.
4. Python appends each result as a `tool` message, using `tool_call_id` to match it to the request.
5. The program calls the model again with the updated history.
6. When the model returns a message without tool calls, the program displays the answer.

In `agent.py`, look at `TOOL_SCHEMAS` for the tool descriptions, `TOOLS` for the function registry, `run_tool()` for execution, and `run_agent()` for the loop. `main()` handles the interactive conversation.

Conversation history is kept in memory for the current session. It is not saved between runs.

## Repository layout

```text
AI_Agent_in_pure_Python/
├── step1.py          # A single API request
├── step2.py          # Interactive chat with message history
├── step3.py          # File-reading tool example
├── agent.py          # Interactive coding agent
├── example.txt       # Sample input for the file-reading example
├── main.py           # Project greeting; not the agent entry point
├── pyproject.toml    # Python requirement and SDK dependency
├── uv.lock           # Dependency lockfile for uv
├── .python-version   # Python 3.13
└── snake_game/       # Separate pygame example
```

### Optional: Snake game

The `snake_game/` folder contains a separate pygame application. It is not required for the agent lessons, and pygame is not included in the project's declared dependencies.

Run it from the repository root with uv:

```bash
uv run --with pygame python -m snake_game
```

Or from your activated virtual environment:

```bash
python -m pip install pygame
python -m snake_game
```

Use the arrow keys or WASD to move, `R` to restart after game over, and `Q` or `Esc` to quit. The game requires a graphical desktop.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Missing or invalid API key | Set `OPENAI_API_KEY` in the current terminal and replace the hardcoded client initializations in Steps 1–3. |
| `ModuleNotFoundError: openai` | Run `uv sync`, or activate your virtual environment and install the SDK. |
| `example.txt` is not found | Launch Step 3 from the repository root. Relative paths resolve from your terminal's working directory. |
| Model access or quota error | Check your API project's model access, billing, and usage limits. |
| A shell command fails | Check the command for your operating system and ensure its required programs are installed. |
| `ModuleNotFoundError: pygame` | Use the optional Snake game installation instructions above. |

## Keep experimenting

Change Step 1's prompt, give Step 2 a system message, or point Step 3 at another sample text file. To extend `agent.py`, add a Python function, register it in `TOOLS`, and describe its arguments in `TOOL_SCHEMAS`.

This is an educational implementation. Useful next improvements include a maximum number of agent iterations, API error handling, argument validation, approval for file writes, and restricting file access to a chosen workspace.

For the API concepts behind these examples, see the [official OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling).
