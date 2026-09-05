from crewai import Task
from .agents import pm, architect, backend_dev, db_engineer #, frontend_dev, db_engineer, sre_engineer

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

# Testing task
test_tooling=Task(
        description="""
        CRITICAL: You are a helpful agent with access to tools. When you need to know how something is done, first examine your common_tools. If they 
         do not fit your purpose, use the 'get_skills' tool to query the tooling knowledge base and find tools related to the topic. 
         Once you retrieve one or more tools, check for the best fit based on semantic content of the description, and use the one that fits best. 
         Do not assume you are a model that should just generate output, but instead apply tools to achieve effects in the codebase.

        Get the 'django-patterns' tool using the 'get_skills' tool. Then, use 'djago-patterns' to provide a review of the codebase of the current project, noting any discrepancies of the current code to best practices.
        """,
        expected_output="A file './_tool_test/tools.md' containing concatenated tooling definitions from files in './.continue/_no_use/'",
        agent=backend_dev
)


# Test get_skills
test_get_skills=Task(
    description="""
    Use the 'get_skills' tool to retrieve a tool for 'accessibility' from the tooling database. 
    
    CRITICAL: When executing this prompt:
    * NEVER retrieve the tool using anything except the 'get_skills' tool that is accessible to you from ./agents/tools.py
    * Print a confirmation to output if the tool was retrieved
    * Print the full content of the retrieved tool to output, never truncate or skip content that is contained in the retrieved tool
    
    """,
    expected_output="Printed confirmations to output if a tool is successfully retrieved.",
    agent=backend_dev
)

setup_postgres=Task(
    description="""
    CRITICAL: When executing this prompt, before doing anything else, use the 'get_skills' tool to query the skills database for 'postgres' skills, and from the response 
    select the tool(s) best fitting what you are trying to do as you start completion of the task. If you need different tools later, query using the 'get_skills' tool, and 
    retrieve other tools you may need. Print which tool is being used when it is being accessed. If a tool call does not complete, fail this task.
    
    Create a new branch 'db_setup' in git
    
    Read postgres related settings in .env, .env.sandbox, ./.my_pgpass, ./.pg_service.conf, ./src/entrypoint.sh, and other files 
    in (sub)folders of ./src/ that are relevant to setting up a database for use with django. Also read the ./docs/database_schema.md. 

    When invoking tools, please specify the invocation path by printing the file or database connection and the tool name(s) used.

    Set up a postgres environment that is consistent between the local machine and the containerized implementation. For the local environment, 
    use the existing postgres installation in /opt/homebrew/bin/postgres. Take the following steps:
    * Adapt ./docker-compose.yml and ./Dockerfile to include the correct postgres version in the backend container. CRITICAL: Ensure all other versions (e.g. python) remain what they currently are.
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
    * Update ./.gitignore by appending any newly created files or folders that should not be versioned, then add all changes in git, then commit the added changes to the 'db_setup' branch
    * Create a pull request for the changes in the 'db_setup' branch, named 'backend-postgres-setup'

    CRITICAL: 
        This task is done once all of the above steps are completed. If one of more steps fail, report these back with detailed information on what went wrong, and how to troubleshoot
        Leave local machine RBAC configuration as-is, and do not make any changes to it. If this prevents successful completion of your task, fail the task and report back the reason.
        Prefer database user 'storesys' for all operations, but make sure to replicate all existing RBAC information from the current local database setup
        Please ensure success on file writes: if output states a file is created or a step completes where files are created (for example creating tests), ensure the file is created. If a file write cannot be validated, fail the task and report the reasons for doing so in the output.
    """,
    expected_output="A pair of postgres databases (local machine and sandbox) that are copies of one another using the same postgres version, RBAC definitions and data model, with all related code consistent, tested and complete.",
    agent=backend_dev
)

# Task for the Developer
initial_db_migrations = Task(
    description="""
    Create a git branch 'db_migrations' and check it out. Push it to the remote server with git push -u origin db_migrations.

    Get postgres-related skill from skill database using get_skill. Then, update the project files with Django models 
    and Serializers in the project directory based on './docs/database_schema.md'. Ensure all fields are validated. 
    Update models.py files for all apps in the project where needed. 

    Ensure changes in the models can be propagated to the backend using './src/manage.py makemigrations' 
    and './src/manage.py migrate'. Write unit tests where needed.
    
    Start or restart the sandbox environment as needed so that the code changes propagate. Run the code in the sandbox environment, validate that it results in a migration file as well as the necessary changes
    in the backend (i.e. verify in postgres that the changes have successfully been applied). 
    
    Run the test suite locally (not in sandbox) and verify that any new and existing unit tests are successfully completed. 
    
    Finally, update './docs/implementation_progress.md':
        * Copy over the high-level steps from './docs/implementation_plan.md'
        * Under the step that mentions database migration (second step of infrastructure setup) add a summary of this task
        * Add code changes to git, and use the summary as the commit message, commit changes to git, push the changes to remote, and create a pull request 
        to merge db_migrations into main. 
    
    This task completes when all steps above have completed. If any of the steps fail, the task also fails. If that happens, 
    print a clear diagnosis for the failure to output.
    
    """,
    expected_output="A set of edited Python files (models.py, serializers.py) for which the code matches ./docs/database_schema, ready for implementation, with unit tests, validation in sandbox, and clear annotation in ./docs/implementation_progress.md and a git commit message. Pull request created.",
    agent=db_engineer
)

product_catalog_services_task = Task(
description="""Create a branch 'product_catalog' and check it out. 
Push it to the remote server with git push -u origin product_catalog.

Your task is to implement the Product and Catalog Services as part of the Service Layer.
The goal is to move logic out of the views and into a dedicated service layer while ensuring 
strict type safety and validation.

Please follow the following Implementation Plan:
1. Schema Definition: Create `apps/products/schemas.py` using Pydantic to define the 
contract for product creation, updates, and variant management.
2. Image Processing & Storage: Implement logic in `apps/products/services.py` or a 
utility module to enforce the .png requirement, handle Pillow-based compression, and 
manage file paths in the media directory.
3. Core Service Logic: Implement `apps/products/services.py` with the following methods:
    - `create_product_listing()`: Handles atomic creation of products and their variants.
    - `get_catalog_data()`: Provides optimized data for the front-end.
    - `update_stock_level()`: Manages inventory updates.
4. Error Handling & Logging: Implement a custom exception layer in `apps/products/exceptions.py` 
and ensure all service actions are logged.

Ensure changes in the models can be propagated to the backend using an appropriate function 
call from django. Write unit tests where planned.
Start or restart the sandbox environment as needed so that the code changes propagate. Run 
the code in the sandbox environment, validate that the created services work.
Run the test suite locally (not in sandbox) and verify that any new and existing unit 
tests are successfully completed. 

Finally, update './docs/implementation_progress.md':
* Under the step that mentions service implementation add a two line summary of this task
* Add code changes to git, and use the summary as the commit message, commit changes to git, push the changes with 'git push origin product_catalog', and create a pull request on the remote to merge product_catalog_services into main. 
This task completes when all steps above have completed. If any of the steps fail, the task also fails. If that happens, print a clear diagnosis for the failure to output.""",
expected_output="product services created, validated and tested, changes on git branch with pull request, progress tracking updated",
agent=backend_dev
)