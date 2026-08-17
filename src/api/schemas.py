from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskResponse(BaseModel):
    """The structure of the initial response when a user starts an agent task."""
    task_id: str
    message: str

class TaskStatus(BaseModel):
    """The structure of the data returned when checking the status of a run."""
    task_id: str
    status: str         # "pending", "running", "completed", or "failed"
    current_step: str    # e.g., "Refining requirements", "Writing code"
    result: Optional[str] = None