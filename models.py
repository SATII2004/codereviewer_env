from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class CodeAction(BaseModel):
    tool: Literal["ls", "read_file", "run_ruff", "run_bandit", "run_pytest", "submit_review"]
    args: Optional[Dict[str, Any]] = None
    verdict: Optional[Literal["approve", "request_changes"]] = None
    comment: Optional[str] = None

class CodeObservation(BaseModel):
    observation: str
    reward: float
    done: bool
    info: Dict[str, Any]