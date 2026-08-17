# Ilumina Studio Database Schema

This document defines the database schema for the Ilumina Studio web application. The design prioritizes modularity, adherence to strict internal standards (no `auto_now`, no dynamic fields), and a clean separation of concerns between storage and logic (Service Layer).

## Overview
The system is built on PostgreSQL. All data modeling follows the principle that state is held in the database rather than the session, ensuring reliability across multiple devices.

---

## 1. Product Catalog Management

### Category
Stores high-level groupings for art pieces.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | Integer/UUID | Primary Key | Unique identifier |
| name | VARCHAR(255) | Not Null | The display name of the category |
| slug | VARCHAR(255) | Unique, Indexed | URL-friendly version of the name |

### Product
Represents a unique art piece available for sale.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | Integer/UUID | Primary Key | Unique identifier |
| category_id | ForeignKey | Not Null | FK to Category |
| title | VARCHAR(250) | Not Null | Name of the artwork |
| description | Text | - | Detailed artist's note / item info |
| base_price | Decimal(10, 2) | Not Null | Price before size multipliers |
| slug | VARCHAR(255) | Unique, Indexed | URL-friendly title |

### ProductVariation
Handles the logic for different canvas sizes (Small, Medium, Large). By separating variation from product, we allow specific pricing for specific dimensions.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | Integer/UUID | Primary Key | Unique identifier |
| product_id | ForeignKey | Not Null | FK to Product |
| size_type | Enum/String | Not Null | 'small', 'medium', 'large' |
| price_modifier | Decimal(10, 2) | Default: 0.00 | Added to base_price for this specific size |

### ProductImage
Handles image assets and metadata.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | Integer/UUID | Primary Key | Unique identifier |
| product_id | ForeignKey | Not Null | FK to Product |
| file_path | VARCHAR(512) | Not Null | Path in storage (date-sensitive folder structure) |
| alt_text | VARCHAR(255) | - | Accessibility text |
| is_primary | Boolean | Default: False | Flag for the main thumbnail shown in lists |

---

## 2. User & Interaction System

### User
Represents a registered customer or an entity seeking information.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | Integer/UUID | Primary Key | Unique identifier |
| email | VARCHAR(255) | Unique, Not Null | Customer's login email |
| first_name | VARCHAR(100) | - | User's given name |
| last_name | VARCHAR(100) | - | User's family name |
| is_commission_client | Boolean | Default: False | Flags users requiring specialized "live" features |

### Contact
Stores messages sent via the "Send a Message" form.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | Integer/UUID | Primary Key | Unique identifier |
| user_id | ForeignKey | Nullable | Link to User (null if anonymous) |
| content | Text | Not Null | The actual message body |
| created_at | Timestamp(6) | Not Null | Time of submission (No auto_now) |

---

## 3. Commerce & Fulfillment

### Cart
Stores active selections made by users during the shopping flow. Values are persisted in the DB for session continuity.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | Integer/UUID | Primary Key | Unique identifier |
| user_id | ForeignKey | Nullable | Link to User (Null if guest) |
| session_token | VARCHAR(255) | Unique, Indexed| Used for identifying guests via cookies/tokens |
| status | String | Not Null | 'active', 'abandoned' |

### CartItem
Links products and specific sizes to a cart.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | Integer/UUID | Primary Key | Unique identifier |
| cart_id | ForeignKey | Not Null | FK to Cart |
| variation_id | ForeignKey | Not Null | FK to ProductVariation |
| quantity | Integer | Default: 1 | Quantity of this specific size selection |

### Order
The finalized transaction record including payment status and shipping details.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| id | Integer/UUID | Primary Key | Unique identifier |
| user_id | ForeignKey | Not Null | The user who placed the order |
| cart_id | ForeignKey | - | Reference to original Cart (if applicable) |
| status | Enum | Not Null | 'placed', 'processing', 'shipped', 'fulfilled', etc. |
| total_amount | Decimal(10, 2) | Not Null | Final calculated price including shipping |
| payment_tx_id | VARCHAR(255) | - | Transaction ID from Stripe/PayPal/iDeal |
| shipment_tracking | VARCHAR(255) | - | Tracking number provided by carrier |

### OrderLogistics
Handles specific physical data for shipments.
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| order_id | ForeignKey | Not Null | FK to Order |
| shipping_address | JSONB | Not Null | {street, city, postal_code, country} |
| billing_address | JSONB | Not Null | {street, city, postal_code, country} |

---

## Implementation Notes & Constraints
1. **Service Layer**: All logic regarding price calculation (base + modifier), order status transitions, and image path generation must reside in `services.py`. `views.py` should only handle request/response parsing.
2. **Strict Migrations**: No dynamic fields or `auto_now` are permitted; all timestamps must be handled at the service layer during creation or update as specified by explicit logic.
3. **REST Compliance**: All database interactions via APIs are exposed through the standard RESTful routes defined in `@api/`.
4. **Identity Mapping**: User-specific items (like "Consult a booking" for commissions) are filtered based on the `is_commission_client` flag within the Service Layer.
