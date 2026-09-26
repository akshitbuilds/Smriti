from ollama import chat

response = chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Smriti AI is working."
        }
    ]
)

print(response.message.content)