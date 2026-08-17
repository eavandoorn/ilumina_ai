# Sandbox Environment Design Specification

## 1. Overview
The goal of this document is to define a sandbox environment for the Ilumina Studio project. The sandbox must provide a functional, representative instance of the webshop where developers and automated agents can validate code changes. It must be easy to spin up, stable, and capable of showing full-stack functionality (Frontend + Backend + Database).

## 2. Objectives
*   **Fidelity**: Must mirror the production environment's logic and state management (Django Service Layer, PostgreSQL backend).
*   **Simplicity**: Start with a minimum viable setup while allowing for easy scaling (e.g., splitting frontend/backend into separate containers later).
*   **Accessibility**: Agents must be able to trigger the sandbox easily as part of their validation loop.

## 3. Technical Requirements & Architecture

### 3.1 Container Strategy
The initial implementation will use a single `sandbox` service in the `docker-compose.yml` to minimize complexity, but it will be structured to allow easy decomposition.
*   **Combined Service**: The first iteration will run both the Django application (serving the frontend via templates/static files) and the PostgreSQL database.
*   **Scaling Path**: The logic is decoupled such that the `web_server` and `db` can be moved into separate containers without changing the internal business logic residing in `services.py`.

### 3.2 Database Persistence
The sandbox must use a persistent volume for the PostgreSQL database to ensure that repeated runs do not lose data unless specifically reset by a migration script or manual intervention.
*   **Engine**: PostgreSQL (as specified in `.Dockerfile`).
*   **Schema Management**: Must utilize Django migrations to initialize state on first run.

### 3.3 Service Layer & Logic
The sandbox must strictly enforce the separation of concerns:
*   `views.py`: Handles only HTTP request logic.
*   `services.py`: Contains all business logic, price calculations, and status transitions.
*   No `auto_now` or dynamic fields in models to ensure schema consistency between development, staging, and production.

## 4. Implementation Plan for Developers

To implement the sandbox based on this design, the following steps are required:

### Step 1: Environment Configuration
Update `.env.example` (or create a `.sandbox.env`) with default configurations for local testing that override production secrets while keeping the database credentials compatible with the Docker environment.

### Step 2: Docker Orchestration
Refine `docker-compose.yml` to support a "dev" or "sandbox" profile.
*   Ensure a `db` service is defined for persistence.
*   The `app` (or `sandbox`) service must mount the `./workspace` directory correctly as per project context.
*   Ports: The sandbox should map port 8000 to be reachable by external tools and browsers.

### Step 3: Initial Data Seeding
Create a script (e.g., managed via python's `management_commands`) to populate the database with standard "seed" data (representative products, categories, and test users) so that automated tests have a predictable state.

### Step 4: Automated Validation Script
Provide a simple shell script or Makefile command (`make sandbox-up` or `sandbox up`) to:
1. Build the containers.
2. Run migrations.
3. Run the seed data script.
4. Start the web server.

## 5. Verification & Validation
To verify that the sandbox is running correctly, a developer or agent can perform the following checks:

### Visual Validation (Manual/Human)
1. Open the browser and navigate to `http://localhost:8000`.
2. Verify that the home page loads with art products from the `product_catalog`.
3. Attempt to add an item to the cart; ensure the total price updates correctly (validating the `service` layer logic).

### Automated Validation (Agent/CI)
An agent successfully validates a change if:
1. The container boots and is listening on port 8000.
2. A curl request to the base URL returns a 200 OK status.
3. A headless browser (Playwright) can navigate through the "Add to Cart" flow in an isolated environment.

## 6. Standards Compliance
*   All code must adhere to `docs/coding_standards.md`.
*   No dynamic fields are allowed in the database schema.
*   The logic for price calculation and status transitions must be encapsulated within `services.py` as defined in `docs/database_schema.md`.
`