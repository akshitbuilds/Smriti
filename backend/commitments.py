from database import get_messages


def extract_commitments():
    messages = get_messages()

    commitments = []

    for message in messages:
        text = message["text"].lower()

        # Poster commitments
        if "poster" in text and ("kal tak" in text or "aaj raat tak" in text):
            if "kal tak" in text:
                deadline = "next day"
            else:
                deadline = "tonight"

            commitments.append({
                "person": message["sender"],
                "task": "Send poster",
                "deadline": deadline,
                "source_message_id": message["id"],
                "source": message["text"],
                "status": "pending"
            })

        # Sponsorship deck
        elif "sponsorship deck" in text and "friday" in text:
            commitments.append({
                "person": message["sender"],
                "task": "Complete sponsorship deck",
                "deadline": "Friday",
                "source_message_id": message["id"],
                "source": message["text"],
                "status": "pending"
            })

    return commitments