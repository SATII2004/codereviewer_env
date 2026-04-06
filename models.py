from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class CodeAction(BaseModel):
    action_type: Literal["view_file", "write_comment", "submit_review"] = Field(..., description="The type of action to take")
    file_path: Optional[str] = Field(None, description="Path to the file to view")
    comment: Optional[str] = Field(None, description="The review comment text")
    verdict: Optional[Literal["approve", "request_changes"]] = Field(None, description="Final status of the PR")

class CodeObservation(BaseModel):
    file_content: Optional[str] = None
    pr_description: str
    current_files: List[str]
    last_action_error: Optional[str] = None

class CodeReward(BaseModel):
    reward: float
    done: bool
    info: dict