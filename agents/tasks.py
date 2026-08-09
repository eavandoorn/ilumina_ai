from crewai import Task

# Task for the Architect
design_task = Task(
    description="""Create a detailed database schema for a webshop including 
    Products, Categories, Orders, and Users. Output should be in Markdown format.""",
    expected_output="A complete markdown document detailing all tables, fields, and relationships.",
    agent=architect
)

# Task for the Developer
coding_task = Task(
    description="""Write the Django models and Serializers based on the 
    architecture provided by the Architect. Ensure all fields are validated.""",
    expected_output="A set of Python files (models.py, serializers.py) ready for implementation.",
    agent=developer
)