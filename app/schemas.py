from pydantic import BaseModel, Field
from typing import Any, Optional, List, Union, Literal

class RunRequest(BaseModel):
    user_id: str = Field(..., description="Stable user id for memory isolation")
    goal: str = Field(..., min_length=5)
    run_id: str | None = Field(None, description="Optional idempotency key; if omitted server generates")

class ToolCall(BaseModel):
    tool_name: str
    args: dict[str, Any] = {}

class AgentStep(BaseModel):
    step: int
    thought: str
    action: Literal["tool", "final"]
    tool_call: ToolCall | None = None
    observation: str | None = None
    final: str | None = None

class RunResponse(BaseModel):
    run_id: str
    status: str
    steps: list[AgentStep]
    final_answer: str


# =========================
# Tool Input Schemas
# =========================

Operand = Union[int, float, str, dict]

class CalculatorArgs(BaseModel):
    expression: Optional[str] = None
    operation: Optional[str] = None
    operands: Optional[List[Operand]] = None

class TextSearchArgs(BaseModel):
    query: str

class DbLookupArgs(BaseModel):
    entity: str

class TextExplainArgs(BaseModel):
    input: str