from database import (
    create_database,
    get_messages,
    get_memories,
    save_memory
)

from extractor import extract_memories
from verifier import verify_memory


print("\n=== SMRITI MEMORY PIPELINE ===\n")


create_database()

messages = get_messages()

print(f"Messages loaded: {len(messages)}")

if not messages:
    print("No messages found.")
    print("Run main.py first.")
    raise SystemExit


print("\nExtracting memories with local AI...\n")

memories = extract_memories(messages)

print(f"Candidate memories: {len(memories)}\n")


verified_count = 0


for memory in memories:

    memory_dict = memory.model_dump()

    verified, reason = verify_memory(
        memory_dict,
        messages
    )

    print("--------------------------------")
    print("TYPE:", memory_dict["type"])
    print("STATEMENT:", memory_dict["statement"])
    print("OWNER:", memory_dict["owner"])
    print("DEADLINE:", memory_dict["deadline"])
    print("SOURCE ID:", memory_dict["source_message_id"])
    print("SOURCE:", memory_dict["source_quote"])
    print("VERIFIED:", verified)
    print("REASON:", reason)

    if verified:
        save_memory(memory_dict)
        verified_count += 1


print("\n================================")
print(f"Verified memories saved: {verified_count}")
print("================================\n")

print("Stored memories:")

for memory in get_memories():
    print(memory)