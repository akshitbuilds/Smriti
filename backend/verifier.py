def verify_memory(memory, messages):
    source_id = memory["source_message_id"]

    source_message = None

    for message in messages:
        if message["id"] == source_id:
            source_message = message
            break

    if source_message is None:
        return False, "Source message not found."

    if memory["source_quote"].strip() != source_message["text"].strip():
        return False, "Source quote does not match the message."

    return True, "Evidence verified."