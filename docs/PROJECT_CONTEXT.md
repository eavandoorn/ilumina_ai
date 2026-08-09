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

# Context mapping
Use the following files for context on the following topics:
* './workspace' is a shared directory that is mounted in the sandbox environment once that is created by running a container with docker-compose.yml 