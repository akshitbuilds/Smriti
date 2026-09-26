"""
main.py
-------
The Smriti FastAPI backend. This is what your frontend (api.js) has
been trying to reach the whole time -- previously nothing implemented
these routes, so every call failed no matter what the API_BASE URL
was.

Run it with:
    uvicorn main:app --reload --port 8000

Then either:
  - point the frontend straight at http://localhost:8000 (recommended
    for local dev, see frontend/.env), or
  - run `ngrok http 8000` and put the printed https URL into
    frontend/.env as VITE_API_BASE if you need a public URL (e.g. to
    demo from your phone or another machine).
"""

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import database
from parser import parse_whatsapp_file
from extractor import build_memories, extract_memories

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_CHAT_PATH = os.path.join(BASE_DIR, "..", "data", "demo_chat.txt")

app = FastAPI(title="Smriti API")

# Allow the Vite dev server (and any origin, for hackathon-speed
# simplicity) to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    database.create_database()

    # Seed from the demo WhatsApp export the first time the DB is empty,
    # so the dashboard has something to show out of the box.
    if database.message_count() == 0 and os.path.exists(DEMO_CHAT_PATH):
        messages = parse_whatsapp_file(DEMO_CHAT_PATH)
        database.save_messages(messages)

    _recompute_memories()


def _recompute_memories():
    messages = database.get_all_messages()
    memories, extracted = build_memories(messages)
    database.save_memories(memories)
    return messages, memories, extracted


# ---------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------

class AskRequest(BaseModel):
    question: str


class ProposeActionRequest(BaseModel):
    type: str
    description: str
    evidence: list = []


# ---------------------------------------------------------------
# Routes
# ---------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "healthy": True}


@app.get("/messages")
def get_messages():
    return database.get_all_messages()


@app.get("/memories")
def get_memories():
    return database.get_all_memories()


@app.get("/commitments")
def get_commitments():
    messages = database.get_all_messages()
    extracted = extract_memories(messages)
    return extracted["commitments"]


@app.get("/decisions")
def get_decisions():
    messages = database.get_all_messages()
    extracted = extract_memories(messages)
    return extracted["decisions"]


@app.get("/conflicts")
def get_conflicts():
    messages = database.get_all_messages()
    extracted = extract_memories(messages)
    return extracted["conflicts"]


@app.get("/weekly-brief")
def get_weekly_brief():
    messages = database.get_all_messages()
    extracted = extract_memories(messages)

    commitments = extracted["commitments"]
    overdue = [c for c in commitments if c["status"] == "OVERDUE"]

    attention = [
        f"{c['person']}: {c['task']} is overdue (was due {c['deadline']})"
        for c in overdue
    ]

    decision_changes_list = [d["statement"] for d in extracted["decisions"]]

    return {
        "commitments": len(commitments),
        "overdue": len(overdue),
        "changes": len(extracted["decisions"]),
        "conflicts": len(extracted["conflicts"]),
        "needs_attention": attention,
        "decision_changes_list": decision_changes_list,
    }


@app.post("/ask")
def ask(payload: AskRequest):
    """
    Very small keyword-matching 'Ask Smriti'. It looks for messages
    whose text shares words with the question and returns the closest
    matches as evidence, plus a one-line synthesized answer.

    This is not an LLM call (no API key required) -- swap this out
    for a real LLM prompt later if you want richer answers; the
    /ask contract (question in, answer + evidence out) won't need to
    change on the frontend.
    """
    messages = database.get_all_messages()
    question_words = {
        w.lower() for w in payload.question.split() if len(w) > 3
    }

    scored = []
    for m in messages:
        text_words = {w.lower().strip(".,?!") for w in m["text"].split()}
        overlap = len(question_words & text_words)
        if overlap > 0:
            scored.append((overlap, m))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    top_matches = [m for _, m in scored[:3]]

    if not top_matches:
        return {
            "answer": "No matching messages found for that question yet.",
            "evidence": [],
        }

    answer = (
        f"Based on the chat history, the most relevant message is from "
        f"{top_matches[0]['sender']}: \"{top_matches[0]['text']}\""
    )

    evidence = [
        {"text": m["text"], "sender": m["sender"], "timestamp": m["timestamp"]}
        for m in top_matches
    ]

    return {"answer": answer, "evidence": evidence}


@app.get("/actions/pending")
def get_pending_actions():
    return database.get_pending_actions()


@app.post("/actions/propose")
def propose_action(payload: ProposeActionRequest):
    action_id = database.create_action(
        payload.type, payload.description, payload.evidence
    )
    return {"id": action_id, "status": "PENDING"}


@app.post("/actions/{action_id}/approve")
def approve_action(action_id: int):
    result = database.approve_action(action_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return {"id": action_id, "status": "APPROVED"}


@app.get("/audit")
def get_audit():
    return database.get_audit_log()
