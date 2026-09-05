import json, os, subprocess

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-5-mini"

SYSTEM_PROMPT = """ You are a coding agent running on the user's terminal.
You can list files, read files, write files, and run shell commands.
User your tools to complete the user's task, then briefly summarize what you did.
The working directory is the folder the user launched you from """


def list_files(path="."):
    try:
        return os.listdir(path)
        entries = []
        for entry in os.scandir(path):
            entries.append(entry.name + ("/" if entry.is_dir() else ""))
        return "\n".join(sorted(entries)) or "(empty directory)"
    except FileNotFoundError:
        return f"Error: The directory '{path}' was not found."

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: The file '{path}' was not found."

def write_file(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to '{path}' ({len(content)} characters)."
    except Exception as e:
        return f"Error writing to '{path}': {str(e)}"

def run_command(command):
    try:
        answer = input(f" Run '{command}'? (y/n): ")
        if answer.strip().lower() != "y":
            return "The user declined to run the command."
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        output = (result.stdout + result.stderr).strip()
        return output or f"(no output, exit code {result.returncode})"
        
    except Exception as e:
        return f"Error running command '{command}': {str(e)}"

TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List the files in a directory. Folders end with /.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory to list, e.g. '.'"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The path to the file to read"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a text file, overwriting if it exists.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The path to the file to write"},
                    "content": {"type": "string", "description": "The content to write to the file"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": (
                'Run a shell command. The user will be prompted for confirmation before running.'
                ' Returns the output of the command, or an error message if it fails.'
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": 'The shell command to run, e.g. `ls -la`'},
                },
                "required": ["command"],
            },
        },
    }
]

def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"  tool: {name}({args}) ")
    try:
        result = str(TOOLS[name](**args))
        return result
    except Exception as e:
        return f"Error running tool '{name}': {str(e)}"

def run_agent(messages):
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            return message.content

        for tool_call in message.tool_calls:
            result = run_tool(tool_call)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Welcome to the AI Agent. Type 'exit' or 'quit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat.")
            break

        messages.append({"role": "user", "content": user_input})
        reply = run_agent(messages)
        print(f"Bot: {reply}")

if __name__ == "__main__":
    main()