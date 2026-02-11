from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models import AgentRun, AgentMessage
from app.schemas import RunRequest, RunResponse, AgentStep
from app.utils.idempotency import new_run_id

from app.tools.registry import ToolRegistry, ToolSpec
from app.tools.calculator import calculator
from app.tools.text_search import text_search
from app.tools.db_lookup import db_lookup
from app.tools.text_explain import text_explain
from app.agent.runner import AgentRunner
from app.schemas import (
    CalculatorArgs,
    TextSearchArgs,
    DbLookupArgs,
    TextExplainArgs,
)

app = FastAPI(title="AI Task Agent (Free Local LLM + Tools + Memory)")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

def build_agent() -> AgentRunner:
    reg = ToolRegistry()

    reg.register(ToolSpec(
        name="calculator",
        fn=calculator,
        input_model=CalculatorArgs,
        description="Performs arithmetic using expression or operation+operands."
    ))

    reg.register(ToolSpec(
        name="text_search",
        fn=text_search,
        input_model=TextSearchArgs,
        description="Returns simulated search results."
    ))

    reg.register(ToolSpec(
        name="db_lookup",
        fn=db_lookup,
        input_model=DbLookupArgs,
        description="Simulated internal DB lookup."
    ))

    reg.register(ToolSpec(
        name="text_explain",
        fn=text_explain,
        input_model=TextExplainArgs,
        description="Converts results into simple explanations."
    ))

    return AgentRunner(reg)

agent = build_agent()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/runs", response_model=RunResponse)
async def create_run(req: RunRequest, db: Session = Depends(get_db)):
    run_id = req.run_id or new_run_id()

    existing = db.get(AgentRun, run_id)
    if existing:
        msgs = db.query(AgentMessage).filter(AgentMessage.run_id == run_id).order_by(AgentMessage.id).all()
        final = next((m.content for m in reversed(msgs) if m.role == "assistant"), "Run exists.")
        return RunResponse(run_id=run_id, status=existing.status, steps=[], final_answer=final)

    run = AgentRun(run_id=run_id, user_id=req.user_id, goal=req.goal, status="running")
    db.add(run)
    db.add(AgentMessage(run_id=run_id, role="user", name=None, content=req.goal))
    db.commit()

    steps_dicts, final_answer = await agent.run(req.user_id, req.goal)

    for s in steps_dicts:
        if s.get("action") == "tool":
            db.add(AgentMessage(run_id=run_id, role="tool", name=s["tool_call"]["tool_name"], content=s.get("observation") or ""))
        if s.get("final"):
            db.add(AgentMessage(run_id=run_id, role="assistant", name=None, content=s["final"]))

    run.status = "completed"
    db.commit()

    steps = [AgentStep(**s) for s in steps_dicts]
    return RunResponse(run_id=run_id, status="completed", steps=steps, final_answer=final_answer)

@app.get("/runs/{run_id}")
def get_run(run_id: str, db: Session = Depends(get_db)):
    run = db.get(AgentRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    msgs = db.query(AgentMessage).filter(AgentMessage.run_id == run_id).order_by(AgentMessage.id).all()
    return {
        "run_id": run.run_id,
        "user_id": run.user_id,
        "goal": run.goal,
        "status": run.status,
        "messages": [{"role": m.role, "name": m.name, "content": m.content, "created_at": str(m.created_at)} for m in msgs],
    }
