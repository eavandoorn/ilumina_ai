# Implementation Plan: Ilumina Studio Webshop

This document outlines the prioritized deliverables and features required to build a Minimum Viable Product (MVP) for the Ilumina Studio webstore, adhering to the specified tech stack and architectural constraints.

## Project Overview
The goal is to create an elegant web store where customers can purchase art prints, manage orders, participate in commissions/live events, and interact with the artist's content.

---

## Deliverables & Feature Roadmap

### 1. Foundation & Core Infrastructure
*Goal: Establish the basic environment, database schema, and project structure.*
- **Infrastructure Setup:**
    - Configure Docker and KinD for local development and CI/CD.
    - Set up the Postgres database via Django migrations (enforcing strict schema rules).
    - Integrate Celery for asynchronous task processing (e.g., email sending).
- **Core Configuration:**
    - Implement Ruff for linting and Black for formatting.
    - Configure OpenTelemetry and Grafana for monitoring/observability.
    - Set up the basic project structure according to the modular design rule.
- **Media Handling:**
    - Implement the image processing pipeline using `Pillow` (handling compression logic).
    - Implement date-sensitive storage logic for images in the `./media/` folder.

### 2. Product Catalog & Management
*Goal: Provide a way to view and browse art pieces.*
- **Product Database:** Create models for paintings, including size variants (Small, Medium, Large) and types (Print vs. Original).
- **Catalog View:** A front-facing list of all paintings/artworks. 
- **Detail View:** Individual painting pages with a "click to enlarge" feature for thumbnails.
- **Media Logic:** Ensure all images rendered are optimized (.png only, no .jpg).

### 3. Shopping Cart & Ordering System
*Goal: Enable customers to select products and initiate the checkout process.*
- **Cart Management:**
    - Functional "Add to Cart" button with size selection and quantity.
    - Backend logic for state management (using Database, not session).
    - Cart View displaying totals and allowing item updates (quantity/removal).
- **Checkout Flow:**
    - Checkout page for inputting shipping and billing information.
    - Integration of payment gateways: Stripe, PayPal, and iDeal/Wero.
- **Order Fulfillment:**
    - Order placement logic (transitioning state from placed to processed, shipped, etc.).
    - Automated email dispatch via Celery containing the invoice upon confirmation.

### 4. User Accounts & Profiles
*Goal: Provide personalization and post-purchase interaction.*
- **Authentication System:** Standard login/register flow using Django's auth system.
- **Customer Portal (Art Print Consumers):**
    - View "Order Overview" with real-time status badges (Processing, Shipped, etc.).
- **Client Portal (Commission/Live Event Clients):**
    - Booking overview for commissions and live events.
    - Terms & Conditions acknowledgement system using a generated PDF format.
    - Signature/Autograph module for contract finalization.

### 5. Engagement & Branding
*Goal: Connect the customer with the artist's presence.*
- **Contact Feature:** A "Send Message" form to contact the artist directly.
- **Social Integration:** Navigation links to the artist’s social media platforms.
- **Content Hub:** A blog post section displaying articles by the artist.

---

## Technical Implementation Notes & Constraints (Architectural Audit)

The following architectural constraints were integrated into the roadmap:
1.  **Service Pattern:** All complex logic is handled in `services.py`; `views.py` remains as barebones wrappers.
2.  **Pydantic Validation:** All API points and data models utilize Pydantic for type hinting and validation.
3.  **Media Logic:** The system only accepts `.png`; automated compression triggers if significant file size reduction is possible without exceeding quality thresholds.
4.  **Asynchronous Tasks:** Non-blocking actions (Emailing, PDF generation) are offloaded to Celery.
5.  **Frontend Structure:** Stylized with Tailwind; components are modular and functional.

## Added Components & Justifications
*Note: No additional components were added beyond the original specification; however, internal system requirements based on architectural constraints were formalized.*
- **Pydantic Implementation:** Integrated to satisfy the requirement for "Type hinting is enforced using pydantic."
- **Celery Integration:** Explicitly mapped to handle asynchronous email delivery and PDF generation tasks.
- **Grafana/OpenTelemetry Monitoring:** Included as a core infrastructure step to meet the observability requirements in the architecture doc.