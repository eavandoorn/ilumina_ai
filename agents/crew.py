from crewai import Crew, Process

# The Crew brings them together
webshop_crew = Crew(
    agents=[architect, developer],
    tasks=[design_task, coding_task],
    process=Process.sequential # Task 1 must finish before Task 2 starts
)

# Execute the plan
result = web_shop_crew.kickoff()
print(result)