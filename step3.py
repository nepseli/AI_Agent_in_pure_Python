import json
from openai import OpenAI

client = OpenAI(api_key="")

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]

messages = [
    {"role": "system", "content": "You are a helpful assistant that can read text files."},
    {"role": "user", "content": "Please read the contents of the file 'example.txt' and summarize it in one sentence."}
]

while True:
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
        tools=TOOL_SCHEMAS,
    )

    message = response.choices[0].message
    messages.append(message)
    print(f"Bot: {message}")

    # No tool calls means the model is done and gave us a normal answer
    if not message.tool_calls:
        print("Bot: " + message.content)
        break

    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        print(f"Model wants to run: read_file({args})")

        result = read_file(**args)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

    
