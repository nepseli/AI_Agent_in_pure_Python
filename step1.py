from openai import OpenAI

client = OpenAI(api_key="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")

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "user", "content": "Explain what an AI Agent is in one sentence."},
    ],
)

print(response.choices[0].message.content)