"""
extractor.py
------------
Turns raw chat messages (from the `messages` table) into structured
team memory: commitments, decisions and conflicts.

This is a lightweight, fully local, rule-based extractor (regex +
keyword heuristics). It needs no API key and no internet access,
which matches the "runs locally / data never leaves the machine"
claim on the dashboard. It is intentionally simple so it's easy to
read and extend -- swap in an LLM call later if you want smarter
extraction, the FastAPI routes in main.py don't need to change.
"""

import re
from collections import defaultdict


# ---------------------------------------------------------------
# Keyword patterns
# ---------------------------------------------------------------

COMMITMENT_PATTERNS = [
    r"\bbhej dunga\b", r"\bbhej doonga\b", r"\bkar dunga\b",
    r"\bkarunga\b", r"\bkarungi\b", r"\bde dunga\b",
    r"\bcomplete karunga\b", r"\bi'?ll\b", r"\bi will\b",
    r"\bwill (do|send|finish|complete|handle|submit|share)\b",
    r"\bpakka\b",
]

COMPLETION_PATTERNS = [
    r"\bbhej diya\b", r"\bkar diya\b", r"\bdone\b", r"\bsent\b",
    r"\bcompleted\b", r"\bsubmitted\b",
]

FOLLOWUP_QUESTION_PATTERNS = [
    r"\bkya hua\b", r"\bkab tak\b", r"\bany update\b", r"\bstatus\b.*\?",
    r"\bhogaya\b\s*\?", r"\bdone\b\s*\?",
]

DECISION_PATTERNS = [
    r"\bfinal\b", r"\bdecided\b", r"\bconfirm(ed)?\b",
    r"\blet'?s (shift|go|move|switch) to\b", r"\bchanged to\b",
    r"\bdone\.?\s*$",
]

CONFLICT_HINT_PATTERNS = [
    r"\balready booked\b", r"\bclash(es)?\b", r"\bconflict\b",
    r"\bnot available\b", r"\boverlap\b", r"\bdouble.?book",
]

DEADLINE_PATTERNS = [
    (r"\baaj raat\b", "Tonight"),
    (r"\bkal\b", "Tomorrow"),
    (r"\baaj\b", "Today"),
    (r"\b(mon(day)?|tue(sday)?|wed(nesday)?|thu(rsday)?|fri(day)?|sat(urday)?|sun(day)?)\b", None),
    (r"\b\d{1,2}\s?(am|pm)\b", None),
    (r"\b\d{1,2}(st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b", None),
]

# words to strip out of a message before treating the remainder as a
# "task name" for a commitment
STRIP_WORDS = COMMITMENT_PATTERNS + [p for p, _ in DEADLINE_PATTERNS] + [
    r"\btak\b", r"\bhona chahiye\b",
]

STOPWORDS = {"the", "a", "an", "to", "for", "on", "in", "at", "and", "ka", "ki", "ke"}


def _matches_any(patterns, text):
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def _extract_deadline(text):
    for pattern, label in DEADLINE_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return label or m.group(0).title()
    return "No deadline"


def _extract_task(text):
    cleaned = text
    for pattern in STRIP_WORDS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[.,!?]+$", "", cleaned).strip()
    words = [w for w in cleaned.split() if w.lower() not in STOPWORDS]
    task = " ".join(words[:6]).strip()
    return task.title() if task else "Unnamed task"


def _topic_keyword(text):
    """
    Very small heuristic to group messages about the same subject,
    e.g. 'venue', 'auditorium', 'hall', 'poster', 'deck'. Used for
    both status tracking (has this task been chased/finished?) and
    conflict detection (do two messages disagree about this topic?).
    """
    candidates = [
        "venue", "auditorium", "hall", "poster", "deck", "sponsorship",
        "budget", "date", "schedule", "room", "ticket",
    ]
    lowered = text.lower()
    for c in candidates:
        if c in lowered:
            return c
    return None


# ---------------------------------------------------------------
# Main extraction
# ---------------------------------------------------------------

def extract_memories(messages):
    """
    messages: list of dicts with keys id, timestamp, sender, text
    (same shape as rows in the `messages` table).

    Returns a dict with commitments, decisions, conflicts -- each a
    list of plain dicts ready to be JSON-serialised by FastAPI.
    """
    commitments_by_key = {}
    open_topic_by_person = {}  # person -> most recent open commitment topic
    decisions = []
    topic_events = defaultdict(list)  # topic -> list of (msg, kind)

    for msg in messages:
        text = msg["text"]
        sender = msg["sender"]
        is_question = text.strip().endswith("?")

        # ---- commitments ----
        if not is_question and _matches_any(COMMITMENT_PATTERNS, text):
            topic = _topic_keyword(text)
            if topic is None:
                # No recognisable subject in this message (e.g. "I'll send
                # it tonight" with no noun) -- assume it continues this
                # person's most recent still-open commitment rather than
                # inventing a new one.
                topic = open_topic_by_person.get(sender, "general")
            open_topic_by_person[sender] = topic
            key = (sender, topic)
            commitments_by_key[key] = {
                "id": f"commit-{sender}-{topic}".lower().replace(" ", "-"),
                "person": sender,
                "task": _extract_task(text),
                "deadline": _extract_deadline(text),
                "status": "PENDING",
                "evidence": text,
                "source_message_id": msg["id"],
                "timestamp": msg["timestamp"],
                "_topic": topic,
            }
            topic_events[topic].append((msg, "commitment"))

        # ---- completion updates an existing commitment ----
        if _matches_any(COMPLETION_PATTERNS, text):
            topic = _topic_keyword(text) or open_topic_by_person.get(sender)
            key = (sender, topic)
            if key in commitments_by_key:
                commitments_by_key[key]["status"] = "COMPLETED"
                commitments_by_key[key]["evidence"] = text

        # ---- a follow-up "any update?" flags the open commitment as overdue ----
        if is_question and _matches_any(FOLLOWUP_QUESTION_PATTERNS, text):
            topic = _topic_keyword(text)
            for key, commitment in commitments_by_key.items():
                if (topic is None or key[1] == topic) and commitment["status"] == "PENDING":
                    commitment["status"] = "OVERDUE"

        # ---- decisions (skip questions -- "Venue confirm hua kya?" is a
        #      question, not a decision, even though it contains "confirm") ----
        if not is_question and _matches_any(DECISION_PATTERNS, text):
            topic = _topic_keyword(text) or "general"
            decisions.append({
                "id": f"decision-{len(decisions) + 1}",
                "statement": text,
                "topic": topic,
                "person": sender,
                "evidence": text,
                "source_message_id": msg["id"],
                "timestamp": msg["timestamp"],
            })
            topic_events[topic].append((msg, "decision"))

        # ---- explicit conflict language ----
        if _matches_any(CONFLICT_HINT_PATTERNS, text):
            topic = _topic_keyword(text) or "general"
            topic_events[topic].append((msg, "conflict_hint"))

    # ---- derive conflicts: any topic with a conflict hint, or with
    #      more than one decision, is worth surfacing ----
    conflicts = []
    for topic, events in topic_events.items():
        has_hint = any(kind == "conflict_hint" for _, kind in events)
        decision_msgs = [m for m, kind in events if kind == "decision"]

        if has_hint or len(decision_msgs) > 1:
            items = [
                {"text": m["text"], "sender": m["sender"], "timestamp": m["timestamp"]}
                for m, _ in events
            ]
            conflicts.append({
                "id": f"conflict-{topic}",
                "title": f"Conflicting information about '{topic}'",
                "topic": topic,
                "status": "CONFLICT",
                "items": items,
            })

    commitments = [
        {k: v for k, v in c.items() if not k.startswith("_")}
        for c in commitments_by_key.values()
    ]

    return {
        "commitments": commitments,
        "decisions": decisions,
        "conflicts": conflicts,
    }


def build_memories(messages):
    """
    Flattens commitments + decisions into one 'memories' list, the
    shape the /memories endpoint returns.
    """
    extracted = extract_memories(messages)

    memories = []

    for c in extracted["commitments"]:
        memories.append({
            "id": c["id"],
            "type": "commitment",
            "statement": f"{c['person']} will handle: {c['task']} ({c['deadline']})",
            "owner": c["person"],
            "deadline": c["deadline"],
            "source_message_id": c["source_message_id"],
            "source_quote": c["evidence"],
            "confidence": 0.7,
            "verified": c["status"] == "COMPLETED",
        })

    for d in extracted["decisions"]:
        memories.append({
            "id": d["id"],
            "type": "decision",
            "statement": d["statement"],
            "owner": d["person"],
            "deadline": None,
            "source_message_id": d["source_message_id"],
            "source_quote": d["evidence"],
            "confidence": 0.6,
            "verified": True,
        })

    return memories, extracted
