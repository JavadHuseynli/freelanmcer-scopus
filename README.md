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
