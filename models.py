from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class CodeAction(BaseModel):
    action_type: Literal["view_file", "submit_review"] = Field(..., description="Action to take")
    file_path: Optional[str] = Field(None, description="Path to the file")
    comment: Optional[str] = Field(None, description="Review feedback")
    verdict: Optional[Literal["approve", "request_changes"]] = Field(None, description="Final PR status")

class CodeObservation(BaseModel):
    file_content: Optional[str] = None
    pr_description: str
    current_files: List[str]
    last_action_error: Optional[str] = None