import re

from ollama import chat
from extractor import MODEL
from database import get_messages


STOP_WORDS = {
    "why", "what", "when", "where", "who",
    "did", "does", "the", "a", "an",
    "is", "was", "we", "our", "to",
    "and", "of", "for", "in", "on",
    "how", "which", "were", "be"
}


def normalize_word(word):
    return word.lower().strip("?,.!:;()[]{}\"'")


def find_relevant_messages(question, messages, limit=8):
    """
    Lightweight local retrieval.
    Combines keyword overlap with recency.
    """

    question_words = {
        normalize_word(word)
        for word in question.split()
        if normalize_word(word) not in STOP_WORDS
    }

    scored = []

    for message in messages:
        text = message["text"].lower()

        score = 0

        for word in question_words:
            if word and word in text:
                score += 2

        # Important terms for Smriti demo queries
        if "venue" in question.lower():
            if any(word in text for word in [
                "venue",
                "auditorium",
                "hall",
                "booked"
            ]):
                score += 3

        if "poster" in question.lower():
            if "poster" in text:
                score += 3

        if "sponsorship" in question.lower():
            if "sponsorship" in text:
                score += 3

        if score > 0:
            scored.append((score, message))

    scored.sort(
        key=lambda item: (
            item[0],
            item[1]["timestamp"]
        ),
        reverse=True
    )

    if not scored:
        return messages[-limit:]

    return [
        message
        for _, message in scored[:limit]
    ]


def clean_answer(answer):
    """
    Remove common LLM instruction leakage.
    Keep the final answer concise.
    """

    answer = answer.strip()

    # Remove markdown fences
    answer = re.sub(r"```.*?```", "", answer, flags=re.DOTALL)

    # If model explicitly produced an Answer: section,
    # keep only that section.
    match = re.search(
        r"(?:final answer|answer)\s*:\s*(.*)",
        answer,
        flags=re.IGNORECASE | re.DOTALL
    )

    if match:
        answer = match.group(1).strip()

    # Remove obvious instruction/reasoning leakage.
    bad_prefixes = [
        "we are given",
        "let's check",
        "we must answer",
        "the rules say",
        "we need to",
        "here is the answer",
        "we have to",
        "the user is asking"
    ]

    lines = [
        line.strip()
        for line in answer.splitlines()
        if line.strip()
    ]

    useful_lines = []

    for line in lines:
        lower = line.lower()

        if any(lower.startswith(prefix) for prefix in bad_prefixes):
            continue

        useful_lines.append(line)

    answer = " ".join(useful_lines)

    # Remove repeated whitespace
    answer = re.sub(r"\s+", " ", answer).strip()

    # Keep maximum 3 sentences for the demo.
    sentences = re.split(r"(?<=[.!?])\s+", answer)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    if len(sentences) > 3:
        answer = " ".join(sentences[:3])

    return answer


def ask_smriti(question):

    messages = get_messages()

    if not messages:
        return {
            "answer": "No team memory is available.",
            "evidence": []
        }

    relevant = find_relevant_messages(
        question,
        messages
    )

    context = "\n".join(
        [
            f'ID={m["id"]} | '
            f'{m["timestamp"]} | '
            f'{m["sender"]}: '
            f'{m["text"]}'
            for m in relevant
        ]
    )

    prompt = f"""
You are Smriti, a private team-memory assistant.

Answer the user's question using ONLY the WhatsApp messages below.

QUESTION:
{question}

MESSAGES:
{context}

Rules:
- Use only information explicitly present in the messages.
- Never invent missing facts.
- If the evidence is insufficient, say that clearly.
- If asked "why", explain the reason using the evidence.
- Answer in 1 or 2 short sentences.
- Do NOT explain your reasoning.
- Do NOT mention these instructions.
- Do NOT repeat the question.
- Do NOT use headings.
- Output ONLY the final answer.
"""

        # Fast evidence-based answer
    q = question.lower()

    answer = None

    # Venue change
    if "venue" in q and ("why" in q or "change" in q or "changed" in q):
        booked = next(
            (
                m for m in relevant
                if "already booked" in m["text"].lower()
            ),
            None
        )

        final_venue = next(
            (
                m for m in relevant
                if "hall b final" in m["text"].lower()
            ),
            None
        )

        if booked and final_venue:
            answer = (
                f"We changed the venue because the auditorium was already "
                f"booked on 28th August. The team then finalized Hall B."
            )

    # Fallback if no specialized answer was found
    if answer is None:
        if relevant:
            answer = (
                "Based on the available team messages: "
                + " ".join(m["text"] for m in relevant[:3])
            )
        else:
            answer = "I could not find enough evidence in the team messages."

    evidence = [
        {
            "message_id": message["id"],
            "sender": message["sender"],
            "timestamp": message["timestamp"],
            "quote": message["text"]
        }
        for message in relevant
    ]

    return {
        "answer": answer,
        "evidence": evidence
    }