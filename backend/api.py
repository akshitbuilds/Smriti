from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import get_memories, get_messages
from ask import ask_smriti

from memory_engine import (
    get_commitment_ledger,
    detect_decision_changes,
    detect_conflicts,
    generate_weekly_brief,
)

from actions import (
    propose_action,
    get_pending_actions,
    approve_action,
    get_audit_log,
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="Smriti",
    description="Sovereign Team Memory API",
    version="1.0.0",
)


# ============================================================
# CORS — LOCAL REACT FRONTEND
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class AskRequest(BaseModel):
    question: str = Field(min_length=1)


class ActionRequest(BaseModel):
    type: str = "general"
    description: str = Field(min_length=1)
    evidence: list[int] = Field(default_factory=list)


# ============================================================
# BASIC
# ============================================================

@app.get("/")
def root():
    return {
        "name": "Smriti",
        "status": "running",
        "mode": "local-first",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Smriti",
        "mode": "local",
        "ai": "evidence-grounded",
    }


# ============================================================
# MEMORY
# ============================================================

@app.get("/memories")
def memories():
    return get_memories()


@app.get("/messages")
def messages():
    return get_messages()


# ============================================================
# ASK SMRITI
# ============================================================

@app.post("/ask")
def ask(request: AskRequest):
    return ask_smriti(request.question)


# ============================================================
# TEAM INTELLIGENCE
# ============================================================

@app.get("/commitments")
def commitments():
    return get_commitment_ledger()


@app.get("/decisions")
def decisions():
    return detect_decision_changes()


@app.get("/conflicts")
def conflicts():
    return detect_conflicts()


@app.get("/weekly-brief")
def weekly_brief():
    return generate_weekly_brief()


# ============================================================
# ACTIONS
# ============================================================

@app.post("/actions/propose")
def propose_action_endpoint(action: ActionRequest):
    return propose_action(
        action.type,
        action.description,
        action.evidence,
    )


@app.get("/actions/pending")
def pending_actions():
    return get_pending_actions()


@app.post("/actions/{action_id}/approve")
def approve_action_endpoint(action_id: int):
    result = approve_action(action_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Action not found",
        )

    return result


# ============================================================
# AUDIT
# ============================================================

@app.get("/audit")
def audit():
    return get_audit_log()