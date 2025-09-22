# Freelancer Marketplace

A Django-based web application that connects clients with freelancers.  
This platform allows users to post projects, place bids, process payments, and leave reviews — providing a complete freelancing ecosystem.

---

## 🚀 Features

- **User Management**
  - User registration, login, and profile management
  - Freelancer and client roles
  - Academic degree and Google Scholar profile support for freelancers

- **Projects**
  - Create, update, delete, and manage projects
  - View detailed project information
  - List of all available projects

- **Bids**
  - Freelancers can place bids on projects
  - Bid details and history view
  - Manage bids per project

- **Payments**
  - Integrated payment system (Stripe support included)
  - Create and track payments
  - Payment details and list views

- **Reviews**
  - Leave reviews for freelancers or clients
  - Review management (create, list, detail)
  - User feedback system for accountability

- **Templates/UI**
  - Base layout with clean Django templates
  - User-friendly pages for projects, bids, payments, reviews, and authentication

---

## 📂 Project Structure

freelancer_marketplace/
│
├── bids/ # Handles bidding functionality
├── payments/ # Payment processing (incl. Stripe integration)
├── projects/ # Project CRUD and management
├── reviews/ # Reviews and ratings system
├── users/ # User management and authentication
├── templates/ # HTML templates for all apps
├── media/ # Uploaded documents and files
├── freelancer_marketplace/ # Main Django project (settings, urls, wsgi, asgi)
└── manage.py # Django management script


---

## 🛠️ Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/freelancer_marketplace.git
   cd freelancer_marketplace


Create a virtual environment

python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows


Install dependencies

pip install -r requirements.txt


Apply migrations

python manage.py migrate


Create a superuser

python manage.py createsuperuser


Run the development server

python manage.py runserver


Visit http://127.0.0.1:8000/ to explore the app.

✅ Requirements

Python 3.10+

Django 4.x+

Stripe (for payment processing)

SQLite3/PostgreSQL/MySQL (any supported DB)

📌 Future Improvements

Advanced search and filtering for projects

Chat/messaging system between clients and freelancers

Project categories & tags

Admin dashboard with analytics

Deployment with Docker

📜 License

This project is licensed under the MIT License.
Feel free to use, modify, and distribute for personal or commercial purposes.




# Freelancer Marketplace Database

This project contains the complete SQL schema for a Freelancer Marketplace platform.  
The database includes **users**, **projects**, **bids**, **payments**, **reviews**, and additional tables required for **Django authentication and admin modules**.

---

## 🔹 Files

- `freelancer_marketplace.sql` — full schema with `CREATE TABLE` statements and foreign key constraints.
- `README.md` — documentation and usage instructions.

---

## 🔹 Usage

### 1. Create a new database
```sql
CREATE DATABASE freelancer_marketplace CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE freelancer_marketplace;
2. Import the SQL file
bash
Copy code
mysql -u root -p freelancer_marketplace < freelancer_marketplace.sql
3. Insert sample data
You can use the following sample inserts to test the database:

sql
Copy code
INSERT INTO users_user (id, username, email, password, is_active, is_staff, is_superuser, date_joined)
VALUES 
(1, 'customer1', 'customer1@mail.com', 'hashed_password', 1, 0, 0, NOW()),
(2, 'freelancer1', 'freelancer1@mail.com', 'hashed_password', 1, 0, 0, NOW());

INSERT INTO projects_project (id, title, description, budget, created_at, updated_at, customer_id)
VALUES 
(1, 'Website Development', 'Build a company website with CMS', 1200, NOW(), NOW(), 1);

INSERT INTO bids_bid (id, project_id, freelancer_id, amount, created_at)
VALUES 
(1, 1, 2, 1000, NOW());

INSERT INTO payments_payment (id, project_id, payer_id, payee_id, amount, status, created_at)
VALUES 
(1, 1, 1, 2, 1000, 'completed', NOW());

INSERT INTO reviews_review (id, project_id, reviewer_id, reviewee_id, rating, comment, created_at)
VALUES 
(1, 1, 1, 2, 5, 'Great work, very professional!', NOW());
🔹 Database Structure
1. Users
users_user → main user table

users_user_groups → user groups

users_user_user_permissions → user permissions

2. Authentication
auth_group

auth_permission

auth_group_permissions

authtoken_token

3. Core Marketplace
projects_project → customer projects

bids_bid → freelancer bids

payments_payment → project payments

reviews_review → project reviews

4. Django Support Tables
django_content_type

django_session

django_migrations

django_admin_log

🔹 Foreign Key Relations
projects_project.customer_id → users_user.id

bids_bid.project_id → projects_project.id

bids_bid.freelancer_id → users_user.id

payments_payment.project_id → projects_project.id

payments_payment.payer_id → users_user.id

payments_payment.payee_id → users_user.id

reviews_review.project_id → projects_project.id

reviews_review.reviewer_id → users_user.id

reviews_review.reviewee_id → users_user.id

🔹 Workflow Example
A customer (users_user) creates a project (projects_project).

A freelancer (users_user) submits a bid (bids_bid).

A payment is made between customer and freelancer (payments_payment).

After completion, both parties can leave a review (reviews_review).

🔹 Notes
The SQL file is designed for MySQL 8.0+.

Tables are based on the Django ORM structure.

For testing purposes, you may add DROP TABLE IF EXISTS ... before each CREATE TABLE.
