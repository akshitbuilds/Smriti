from datetime import datetime, timedelta
from database import get_messages


def parse_timestamp(timestamp):
    return datetime.fromisoformat(timestamp)


def resolve_deadline(message):
    """
    Resolve simple relative deadlines using the message timestamp.
    """

    text = message["text"].lower()
    message_date = parse_timestamp(message["timestamp"])

    if "kal tak" in text:
        return (message_date + timedelta(days=1)).date().isoformat()

    if "aaj raat tak" in text:
        return message_date.date().isoformat()

    if "friday" in text:
        days_until_friday = (4 - message_date.weekday()) % 7

        if days_until_friday == 0:
            days_until_friday = 7

        return (
            message_date + timedelta(days=days_until_friday)
        ).date().isoformat()

    return None


def extract_commitment_records():
    messages = get_messages()

    records = []

    for message in messages:
        text = message["text"].lower()

        if "poster" in text and (
            "kal tak" in text or
            "aaj raat tak" in text
        ):
            records.append({
                "person": message["sender"],
                "task": "Send poster",
                "deadline": resolve_deadline(message),
                "source_message_id": message["id"],
                "source": message["text"]
            })

        elif "sponsorship deck" in text and "friday" in text:
            records.append({
                "person": message["sender"],
                "task": "Complete sponsorship deck",
                "deadline": resolve_deadline(message),
                "source_message_id": message["id"],
                "source": message["text"]
            })

    return records


def normalize_commitments():
    records = extract_commitment_records()

    normalized = {}

    for record in records:

        key = (
            record["person"],
            record["task"],
            record["deadline"]
        )

        if key not in normalized:
            normalized[key] = {
                "person": record["person"],
                "task": record["task"],
                "deadline": record["deadline"],
                "source_message_ids": [],
                "evidence": []
            }

        normalized[key]["source_message_ids"].append(
            record["source_message_id"]
        )

        normalized[key]["evidence"].append(
            record["source"]
        )

    return list(normalized.values())


def commitment_status(commitment):
    if not commitment["deadline"]:
        return "NO_DEADLINE"

    deadline = datetime.fromisoformat(
        commitment["deadline"]
    ).date()

    today = datetime.now().date()

    if deadline < today:
        return "OVERDUE"

    return "PENDING"


def get_commitment_ledger():
    commitments = normalize_commitments()

    for commitment in commitments:
        commitment["status"] = commitment_status(commitment)

    return commitments


def detect_decision_changes():
    messages = get_messages()

    changes = []

    venue_messages = [
        m for m in messages
        if (
            "auditorium" in m["text"].lower()
            or "hall b" in m["text"].lower()
        )
    ]

    if venue_messages:
        old_decision = None
        new_decision = None
        reason = None
        evidence = []

        for message in venue_messages:
            text = message["text"].lower()

            if "available" in text and "auditorium" in text:
                old_decision = "Auditorium"

            if "already booked" in text:
                reason = message["text"]

            if "hall b final" in text:
                new_decision = "Hall B"

            if "shift to hall b" in text:
                new_decision = "Hall B"

            evidence.append({
                "message_id": message["id"],
                "sender": message["sender"],
                "timestamp": message["timestamp"],
                "quote": message["text"]
            })

        if old_decision and new_decision:
            changes.append({
                "type": "decision_change",
                "topic": "Venue",
                "from": old_decision,
                "to": new_decision,
                "reason": reason,
                "evidence": evidence
            })

    return changes


def detect_conflicts():
    messages = get_messages()

    conflicts = []

    poster_messages = [
        m for m in messages
        if "poster" in m["text"].lower()
    ]

    if len(poster_messages) >= 2:
        deadlines = []

        for message in poster_messages:
            deadline = resolve_deadline(message)

            if deadline:
                deadlines.append({
                    "message": message,
                    "deadline": deadline
                })

        if len(deadlines) >= 2:
            first = deadlines[0]
            last = deadlines[-1]

            if first["deadline"] != last["deadline"]:
                conflicts.append({
                    "type": "commitment_update",
                    "topic": "Poster deadline",
                    "previous_deadline": first["deadline"],
                    "new_deadline": last["deadline"],
                    "evidence": [
                        {
                            "message_id": first["message"]["id"],
                            "quote": first["message"]["text"]
                        },
                        {
                            "message_id": last["message"]["id"],
                            "quote": last["message"]["text"]
                        }
                    ]
                })

    return conflicts


def generate_weekly_brief():
    commitments = get_commitment_ledger()
    changes = detect_decision_changes()
    conflicts = detect_conflicts()

    overdue = [
        c for c in commitments
        if c["status"] == "OVERDUE"
    ]

    pending = [
        c for c in commitments
        if c["status"] == "PENDING"
    ]

    return {
        "summary": {
            "total_commitments": len(commitments),
            "overdue": len(overdue),
            "pending": len(pending),
            "decision_changes": len(changes),
            "conflicts": len(conflicts)
        },
        "overdue_commitments": overdue,
        "pending_commitments": pending,
        "decision_changes": changes,
        "conflicts": conflicts
    }