# Project goal:
Develop a simple yet elegantly designed web store called Ilumina Studio, where customers can:
* Buy art prints of a number of paintings in sizes small, medium and large by
    * Clicking a thumbnail to see a larger picture
    * Adding the picture to a cart with size selection and quantity, displaying a total price;
    * Reviewing the cart in a cart view allowing updates of any item in the cart;
    * Placing the order with a button in the cart;
    * Inputting shipping information and billing information;
    * Paying for the order using payment flows to Stripe, PayPal, and iDeal / Wero;
    * Upon payment confirmation receiving an order placement e-mail with invoice, and visual confirmation on screen;
* Log into a personal page:
    * If art print consumer:
        * consult an order overview with order status  (placed, processing, shipped, fulfilled, return transit, return received, canceled)
    * If live painting / commission consumer: 
        * consult a booking overview with bookings
        * Confirm terms and conditions for commission painting or live event painting using a generated pdf file and an autograph module
* Consult a catalog of paintings by the artist
* Send a message to the artist
* Click links to visit the artist's socials
* Read blog posts by the artist

# Tech stack
The project uses:
* Python
    * django framework for web store structure
* Tailwind
    * CSS for styling 
* Postgres for backend database
* Docker for CI / CD
* KinD for containerization

# Architectural decisions
* Source code for the project is located in the ./src/ folder
* The project uses uv for python environment and package management
* API endpoints should confirm to REST specification
* API communication is handled using Django Rest Framework
* All code is linted using ruff
* All tests are written in playwright and added to the /tests/ folder
* All code is formatted using the python module black
* .png files are compressed using pillow using quality between 75 and 80 if:
  * They have not been compressed before, and
  * A substantial reduction in image file size results
* .jpeg files are not used in this webshop
* Database migrations are strict and based only on Django models
* Data models cannot include auto_now or dynamic fields
* The database, rather than the user session, is where user related state is kept
* Celery is used for asynchronous processing of non-blocking tasks
* Tailwind is used for styling
* Any implemented step needs to be tested and documented before further development can take place
* Within app folders, 'views.py' files contain only barebones views. Any logic needed for processing state is contained in the 'services.py' file within the app folder instead.
* Use functional components
* Use a modularized approach and decompose to a suitable level of abstraction whenever possible
* All functions have clear, but concise documentation
* Type hinting is enforced using pydantic, and data correspondence is checked using pydantic
* All created code is tested for validation in a sandbox environment, that can be created using the './docker-compose.yml' file
* If the sandbox environment is not sufficient for a test run, agents do not directly adapt it in './docker-compose.yml' or otherwise, the user is always prompted to change any configurations or parameters for the sandbox environment.
* Any images used in the webshop are stored in a folder structure that is date-sensitive when they are loaded for the first time
* Grafana's open source monitoring / observability tool is used for performance monitoring, and performance metrics, logs and traces are collected following OpenTelemetry standards

# Context mapping
Use the following files for context on the following topics:
* './docker-compose.yml and './.Dockerfile' create a docker sandbox environment that agents can use to validate code changes
* './src' contains all source code needed to build the webshop django app as a containerized service
* './docs/PROJECT_CONTEXT.md' is the current file, it contains an overview of the project context that agents can use to get an idea of the project goal, tech stack, architectural decisions and files
* './docs/coding_standards.md' contains coding standards all code in the project should adhere to where relevant
* './docs/database_schema.md' provides an overview of the structure and contents of the postgres backend used for this project
* './src/core/' contains project level components of the python Django framework for the webshop.
* './src/orders/', './src/products/' and './src/users/' contain app-level components of the python Django framework for the webshop
* './src/media/' contains all media (e.g. image files) for use in the webshop
* './src/templates/' and './src/static' contains all html templates and static files for the frontend of the webshop
* './tests/' contains all playwright tests for the webshop
* './src/theme/' contains all css and tailwind files necessary for styling the webshop
* './scripts' contains all one-of migration or data scripts for the project
* './agents' contains all configuration related information for agents working on this project. This information is intended purely as instruction for agents. This folder should not normally be operated on directly by agents
* './.venv/', './.continue/' and './.github/' contain logic related to the operation of development stack middleware. These folders should not normally be operated on by agents directly
* './src/api/' contains the interface by which agents can act upon webshop logic. Logic in this folder can be operated upon by agents occasionally, but is not part of the webshop functionality
* './src/entrypoint.sh' contains the entrypoint logic for provisioning the app inside a containerized environment
* './Modelfile' contains a mapping to enable Gemma 4 tool calling. This file should never be changed or removed