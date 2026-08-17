from fastapi import APIRouter, BackgroundTasks
from .schemas import TaskResponse, TaskStatus
from .workers import run_worker, task_db # Import the worker logic and state
import uuid

router = APIRouter()

@router.post("/start-task", response_model=TaskResponse)
async def start_task(background_tasks: BackgroundTasks):
    # 1. Generate a unique ID for this specific agent run
    task_id = str(uuid.uuid4())
    
    # 2. Initialize the status in our database/memory
    task_db[task_id] = {
        "status": "pending",
        "current_step": "Initializing",
        "result": None
    }
    
    # 3. Hand off to the worker so the API can return immediately
    background_tasks.add_task(run_worker, task_id)
    
    return {"task_id": task_id, "message": "Agent process started."}

@router.get("/status/{task_id}", response_model=TaskStatus)
async def get_status(task_id: str):
    # Check if the ID exists in our worker's record
    task = task_db.get(task_id)
    if not task:
        return {"error": "Invalid Task ID"}
    
    return {
        "task_id": task_id,
        "status": task["status"],
        "current_step": task["current_step"],
        "result": task.get("result")
    }