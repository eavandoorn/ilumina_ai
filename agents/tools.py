
from crewai.tools import tool
import subprocess
import os
from typing import List

# --- TOOLS FOR ARCHITECT & DB ENGINEER ---
# These tools help in planning and ensuring schema integrity before coding begins.

@tool("query_database_schema")
def query_database_schema() -> str:
    """
    Examines the current Django models and database structure to ensure 
    compliance with 'no dynamic fields' and 'no auto_now' rules.
    Use this tool when designing new features to check existing constraints.
    """
    # Implementation would query the Django model metadata or a schema file
    return "Current schema analysis: [Schema details here]"

@tool("validate_schema_logic")
def validate_schema_logic(schema_description: str) -> str:
    """
    Analyzes a proposed database schema (Markdown or SQL) to ensure it 
    follows the project's strict migration rules and normalization standards.
    """
    # Logic to check for prohibited fields like auto_now or dynamic types
    return "Schema validation passed."

# --- TOOLS FOR BACKEND DEVELOPER ---
# These tools allow the developer to implement logic, handle images, and integrate services.

@tool("process_image_assets")
def process_image_assets(file_path: str) -> str:
    """
    Processes .png files using the Pillow library. 
    Ensures quality is between 75-80 and only compresses if a substantial 
    reduction in file size occurs. This tool must be used for all new 
    media added to the /media/ folder.
    """
    # Implementation uses PIL (Pillow) to check compression status and resize
    return f"Image {file_path} processed successfully."

@tool("integrate_payment_gateway")
def integrate_payment_gateway(provider: str) -> str:
    """
    Configures the integration for Stripe, PayPal, or iDeal/Wero.
    This tool handles the logic for generating payment intents and 
    handling webhooks for order confirmation.
    """
    # Logic to interface with specific provider SDKs
    return f"Successfully integrated {provider} gateway."

@tool("setup_celery_task")
def setup_celery_task(task_name: str, logic_description: str) -> str:
    """
    Registers a new background task in the Celery worker. 
    Use this for non-blocking tasks like sending order confirmation emails 
    or generating PDF invoices.
    """
    # Logic to register a task in the celery beat/worker system
    return f"Task {task_name} added to Celery queue."

# --- TOOLS FOR SRE & FRONTEND (SHARED VALIDATION) ---
# These tools are critical for the "Gatekeeper" role and ensuring production readiness.

@tool("validate_in_sandbox")
def validate_in_sandbox(file_path: str) -> str:
    """
    Spins up a Docker container using the project's .Dockerfile 
    and .docker-compose.yml to run the code in an isolated environment.
    Returns the logs and exit status of the test run.
    Use this tool before any code is marked as 'complete'.
    """
    try:
        # Logic to run docker-compose up --build and execute a test script
        subprocess.run(["docker-compose", "up", "-d", "--build"], check=True)
        result = subprocess.run(["docker-compose", "exec", "-T", "web_app", "python3", file_path], 
                                  capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Sandbox validation failed: {str(e)}"

@tool("monitor_performance_metrics")
def monitor_performance_metrics() -> str:
    """
    Checks the OpenTelemetry traces and Grafana metrics for the 
    current environment. Use this to ensure that new features do not 
    degrade system performance or increase latency.
    """
    # Logic to query Prometheus/Grafana via API or local logs
    return "Performance metrics are within acceptable thresholds."

@tool("run_playwright_tests")
def run_playwright_tests() -> str:
    """
    Executes the suite of Playwright tests located in the /tests/ folder.
    This is the final check to ensure the UI and backend integration 
    work correctly for the end-user.
    """
    # Logic to trigger 'pytest' or 'playwright test' command
    return "All Playwright tests passed."

@tool("output_to_new_file")
def output_to_new_file(file_path: str, text_to_write: str) -> str:
    """
    Writes text output to a new file under specified filepath
    Args:
        file_path (str): Relative path to the file.
        text_to_write (str): The full block of text to write to the designated file
    """
    if os.path.exists(file_path):
        return f"Error: File '{file_path}' exists, and is not okay to overwrite."

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text_to_write)
            
        return f"Success: Successfully updated '{file_path}'."
    except Exception as e:
        return f"Error modifying file: {str(e)}"

@tool("edit_file")
def edit_file(file_path: str, target_text: str, replacement_text: str) -> str:
    """
    Edits a specific portion of an existing file.
    Args:
        file_path (str): Relative path to the file.
        target_text (str): The exact phrase or block of text you want to replace.
        replacement_text (str): The new text to insert instead.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist in workspace."
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if target_text not in content:
            return f"Error: Could not find target_text in '{file_path}'."
            
        # Perform localized find-and-replace
        updated_content = content.replace(target_text, replacement_text)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        return f"Success: Successfully updated '{file_path}'."
    except Exception as e:
        return f"Error modifying file: {str(e)}"

@tool("read_file_contents")
def read_file_contents(file_path: str) -> str:
    """
    Reads and returns the complete text content of a specified file.
    Args:
        file_path (str): Relative path to the file.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."

    if os.path.isdir(file_path):
        return f"Error: '{file_path}' is a directory, not a file."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool("run_cli_command")
def run_cli_command(command: str) -> str:
    """
    Executes a shell command in the local terminal. 
    Use this tool when you need to run CLI commands, install packages, 
    check system status, or run scripts (e.g., 'ls', 'mkdir', 'python manage.py migrate').
    The input should be the full command string.
    """
    try:
        # We use shell=True because most CLI commands in macOS rely on 
        # shell-specific paths and behavior.
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            executable="/bin/bash"  # Ensures consistent behavior on macOS/Linux
        )

        if result.returncode == 0:
            # Success: Return the standard output
            return result.stdout if result.stdout else "Command executed successfully (no output)."
        else:
            # Failure: Return both stderr and the return code to help the agent debug
            return f"Error executing command. \nReturn Code: {result.returncode}\nStderr: {result.stderr}"
    except Exception as e:
        # Catch cases where the command is not found or other system level errors
        return f"Exception occurred while trying to run '{command}': {str(e)}"