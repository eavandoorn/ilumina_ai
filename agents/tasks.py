from crewai import Task
from .agents import pm, architect, backend_dev #, frontend_dev, db_engineer, sre_engineer

# Create Implementation Plan
planning_task = Task(
    description="""Read the webshop description in './docs/PROJECT_CONTEXT.md'. 
    Convert the 'Project goal' into a set of deliverables for a minimum viable webshop, ensure they follow a logical order of progression for implementation, and list them.
    Then, for each deliverable, identify which features and steps need to be implemented, and list these under that deliverable. Critical: Treat the Tech 
    stack and Architectural decisions sections as constraints in formulating the deliverables, and ensure they are all accounted for. If any elements are added to the tech 
    stack, provide a brief rationale for the additions and choices at the end of the output.
    
    Write the resulting plan to a new file './docs/implementation_plan.md'
""",
expected_output="A markdown document detailing project deliverables and featuresfor implementing a webshop for Ilumina Studio",
agent=pm
)

# Design Data Model
design_task = Task(
    description="""Read the webshop description in './docs/PROJECT_CONTEXT.md' and the model files './scripts/old_project_staging/old_models.py'
    and './scripts/old_project_staging/old_product_models.py' Create a design for a database schema for the Ilumina Studio webshop, that enhances 
    the files from the previous project with any necessary additions or changes, and ensures that architecture best practices are followed. 
    Output should be in Markdown format. The schema should include Product, Product Image, User, Category, Order, Cart, CartItem and Contact.
    
    Critical: Use the 'output_to_new_file' tool to write output to the file './docs/database_schema.md' 
    Confirm that this command has successfully completed, or if not, report why it has not. 
    """,
    expected_output="A complete markdown document detailing all tables, fields, and relationships, written to the designated file.",
    agent=architect
)

# Design sandbox
sandbox_design=Task(
    description="""Check if a file './docs/sandbox_design.md' exists. If it does, consider this task completed and move on to the next task. If it does not, read the webshop description in './docs/PROJECT_CONTEXT.md', the database schema in './docs/database_schema.md', and 
'./Dockerfile' and './docker-compose.yml'. Create a design for a sandbox environment with the following requirements:
* The sandbox should be fully representative of the deployed webshop, and should enable validation via browser when it is running
* The sandbox should follow the principle of minimum viable solution, but should be extensible in the future (e.g. have one container deployed initially, but with the possibility to separate the backend into a separate containerized service or create a second frontend contianer with a load balancer)
* Agents working on the current project should be able to invoke the sandbox as part of validating code

Critical: write a specification for what should be implemented, that a developer could pick up and implement. Ensure this specification conforms to the specifications and decisions in './docs/PROJECT_CONTEXT.md'. Include a brief description of how to validate that the sandbox is running in the output. Output this in markdown format, into a new file './docs/sandbox_design.md'.
""",
expected_output="A markdown file './docs/sandbox_design.md', that holds an implementation plan for a reusable sandbox environment.",
agent=architect
)

# Set up Docker and KinD
setup_sandbox=Task(
    description="""Read './.Dockerfile', './docker-compose.yml', and './docs/sandbox_design.md'. Adapt ./.Dockerfile and ./docker-compose.yml if necessary so that 
    they form a functional sandbox that developers can use to test whether the webshop is working as planned. If any other code needs to be written to do so,
    write / edit it as needed. 
    Critical: Ensure the files cover the requirements set out in the ./docs/sandbox_design.md file.
    Critical: Write the changes to any files 
    Critical: Validate instructions to run the sandbox by conducting a test run and validating 
    that the webshop functions in the container like it would in the current setup.
    Critical: Ensure uv is used to manage the environment incide the sandbox. If the sandbox environment expects a 'requirements.txt' file, export the current environment setup to file by running 'uv export --format requirements.txt' """,
    expected_output="Updated ./.Dockerfile and ./docker-compose.yml with validated sandbox, or a description of code to be produced before a sandbox is in place.",
    agent=backend_dev
)

# Set up Postgres
setup_postgres=Task(
    description="""Read postgres related settings in .env, .env.sandbox, ./.my_pgpass, ./.pg_service.conf, ./src/entrypoint.sh, and other files 
    in (sub)folders of ./src/ that are relevant to setting up a database for use with django. Also read the ./docs/database_schema.md. 

    Set up a postgres environment that is consistent between the local machine and the containerized implementation. For the local environment, 
    use the existing postgres installation in /opt/homebrew/bin/postgres. Take the following steps:
    * Adapt ./docker-compose.yml and ./Dockerfile to include the correct postgres version in the backend container
    * Use the existing credentials for the local machine postgres and change the data model on the local machine to match the model described in ./docs/database_schema.md
    * Adapt ./docker-compose.yml and ./Dockerfile to replicate the database on the local machine in the sandbox:
        * Extract RBAC-related configuration from the database on the local machine and add it to ./docker-compose.yml and ./Dockerfile securely
        * Replicate the data model implemented on the local machine for the sandbox instance
    * Run the sandbox environment, and ensure:
        * The database is running and can be accessed
        * The database RBAC configuration is as expected
        * The database data model is as expected
        * Any findings are reported back
    * Write unit tests for database provisioning and add them to the './tests/ folder in a sensibly named subfolder
        * Include tests for the database on the local machine and the sandbox
        * Include tests for setup of RBAC and data model
        * Use playwright for writing and running the tests
    * Run the tests and verify they are completed successfully
    * Validate there are no remaining inconsistencies in any files that were edited in configuring and running the database
    * Create a pull request for the changes named 'backend-postgres-setup'

    CRITICAL: 
        This task is done once all of the above steps are completed. If one of more steps fail, report these back with detailed information on what went wrong, and how to troubleshoot
        Leave local machine RBAC configuration as-is, and do not make any changes to it. If this prevents successful completion of your task, fail the task and report back the reason.
        Prefer database user 'storesys' for all operations, but make sure to replicate all existing RBAC information from the current local database setup
    """,
    expected_output="A pair of postgres databases (local machine and sandbox) that are copies of one another using the same postgres version, RBAC definitions and data model, with all related code consistent, tested and complete.",
    agent=backend_dev
)



# # Task for the Developer
# coding_task = Task(
#     description="""Write the Django models and Serializers based on the 
#     architecture provided by the Architect. Ensure all fields are validated. 

#     Use the 'edit_file' tool to add the resulting code to the correct models.py and serializers.py files
#     for each app where they need to be added.
#     """,
#     expected_output="A set of Python files (models.py, serializers.py) ready for implementation.",
#     agent=backend_dev
# )