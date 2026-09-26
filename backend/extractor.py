from typing import Optional

from ollama import chat
from pydantic import BaseModel


MODEL = "qwen3:4b"


class MemoryItem(BaseModel):
    type: str
    statement: str
    owner: Optional[str] = None
    deadline: Optional[str] = None
    source_message_id: int
    source_quote: str


class MemoryExtraction(BaseModel):
    memories: list[MemoryItem]


def extract_memories(messages):

    formatted_messages = []

    for message in messages:
        formatted_messages.append(
            f'ID={message["id"]} | '
            f'{message["timestamp"]} | '
            f'{message["sender"]}: '
            f'{message["text"]}'
        )

    conversation = "\n".join(formatted_messages)

    prompt = f"""
You are Smriti, a private sovereign team-memory system.

Analyze the WhatsApp messages below.

Extract useful memories from the conversation.

Look for:

1. commitments
2. deadlines
3. decisions
4. important team facts

Rules:

- Never invent information.
- Every memory must have a source_message_id.
- source_message_id must exactly match one of the provided IDs.
- source_quote must be copied EXACTLY from the corresponding message.
- If the deadline is unclear, use null.
- If the owner is unclear, use null.
- Keep statements short.
- Only extract information explicitly supported by the messages.
- Do not create memories from casual conversation.

WhatsApp messages:

{conversation}
"""

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=MemoryExtraction.model_json_schema(),
        think=False,
        options={
            "temperature": 0
        }
    )

    print("\nAI response received.")

    content = response.message.content

    print("AI response length:", len(content))

    print("\nParsing structured memories...")

    result = MemoryExtraction.model_validate_json(content)

    print("Structured extraction successful.")

    return result.memories