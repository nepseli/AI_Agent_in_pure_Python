from openai import OpenAI

client = OpenAI(api_key="")

messages = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat.")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
    )

    reply = response.choices[0].message.content
    print(f"Bot: {reply}")

    messages.append({"role": "assistant", "content": reply})
