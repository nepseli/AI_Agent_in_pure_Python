from openai import OpenAI

client = OpenAI(api_key="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")

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