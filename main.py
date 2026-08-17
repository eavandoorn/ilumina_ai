from dotenv import load_dotenv
from agents.agents import architect, db_engineer, backend_dev, frontend_dev, sre_engineer
from agents.tasks import design_task, planning_task # and other tasks
from agents.crew import web_shop_crew

load_dotenv()

if __name__ == "__main__":
    # This is the actual entry point. 
    # You run this from your terminal: python main.py
    print("🚀 Starting Ilumina Studio Development Mission...")
    result = web_shop_crew.kickoff(inputs={
        "initial_goal": "Build the shopping cart and payment gateway for Ilumina Studio."
    })
    print(result)