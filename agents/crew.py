from crewai import Crew, Process
from .tasks import setup_postgres, test_tooling, test_get_skills, initial_db_migrations
from .agents import architect, db_engineer, backend_dev, frontend_dev, sre_engineer


# The Crew brings them together
web_shop_crew = Crew(
    agents=[architect, db_engineer, backend_dev, frontend_dev, sre_engineer],
    tasks=[initial_db_migrations], #[design_task, planning_task, ..., ...]
    process=Process.sequential # Task 1 must finish before Task 2 starts
)

# Execute the plan
# result = web_shop_crew.kickoff() ## Done in main.py
