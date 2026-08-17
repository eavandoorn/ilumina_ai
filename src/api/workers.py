from datetime import datetime
# Import your actual crew from your agents folder
from agents.crew import RUN_AGENT_WORKFLOW 

# In a production app, replace this dict with a database call (e.g., SQLAlchemy or Redis)
# This persists the state so it can be retrieved by the routes.py file.
task_db = {}

def run_worker(task_id: str):
    """
    This function is executed by FastAPI's BackgroundTasks. 
    It does not block the web request.
    """
    # Update state to 'running'
    task_db[task_id]["status"] = "running"
    task_db[task_id]["current_step"] = "Executing CrewAI Logic"

    try:
        # This calls your actual Agentic logic (CrewAI)
        result = RUN_AGENT_WORKFLOW() 
        
        # Update status to success
        task_db[task_id]["status"] = "completed"
        task_db[task_id]["result"] = result
    except Exception as e:
        task_db[task_id]["status"] = "failed"
        task_db[task_id]["result"] = str(e)