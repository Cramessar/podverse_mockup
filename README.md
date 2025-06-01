# Podverse Mockup - Admin Dashboard & Backend

## Overview

This project provides an admin dashboard and backend API for the Podverse podcast platform. It includes:

- A React/Next.js based frontend for admin login and dashboard UI
- A FastAPI backend serving RESTful admin API endpoints with OpenAPI/Swagger docs
- Firebase authentication for admin login using Google OAuth
- A local SQLite database seeded with realistic dummy data for development and testing
- Robust API endpoints for managing users, podcasts, episodes, and analytics
- OpenAPI specification in `openapi.yaml` with detailed schema and endpoint definitions
- Docker support and environment configurations for streamlined local development

This is all subject to change. This is just to help us get started.

---

## Project Structure

```
├── backend/ # Backend API and data seeding scripts currently #this is where the python files live
│ ├── main.py # FastAPI app entry point
│ ├── routes.py # API endpoint definitions
│ ├── models.py # SQLAlchemy models
│ ├── database.py # Database connection setup
│ ├── seed_data.py # Dummy data generator
│ └── openapi.yaml # OpenAPI spec for API docs
│
├── pages/ # Next.js frontend pages (admin login, dashboard)
│ ├── admin/
│ │ ├── index.tsx # Admin login page with Firebase Google OAuth
│ │ ├── dashboard.tsx # Admin dashboard UI
│ │ └── utils/
│ │ ├── firebaseClient.ts # Firebase auth helper
│ │ └── useAdminAuth.tsx # Custom React hook for admin auth state
│
├── public/ # Static assets (logos, icons, etc.) #main site 
├── package.json # Frontend dependencies and scripts
├── requirements.txt # Backend Python dependencies
├── .env.example # Environment variable template
└── README.md # This file
```

---

## Getting Started

### Prerequisites

```
- Node.js (v18+)
- Python 3.10+
- SQLite (optional: included as a file-based DB)
- Firebase project for authentication (Google OAuth setup)
- Environment variables configured (see `.env.example`) 
#you will need to create a .env.local file. you can copy and paste the contents from .env.example
```
---

### Setup Frontend

```
run these commands in the project root 
This is an example PS C:\Users\chris\OneDrive\Documents\GitHub\podverse_mockup> 

npm install
This will install the package.json. think of this as your requirements.txt for react.

npm run dev
Open http://localhost:3000/ to access the main page. 
Admin page is here http://localhost:3000/admin
```

---

### Setup Backend

```
cd backend 
This is another example of what you should see PS C:\Users\chris\OneDrive\Documents\GitHub\podverse_mockup\backend>

pip install -r requirements.txt

python seed_data.py       # Seed SQLite DB with dummy data

uvicorn main:app --reload

Backend API runs on http://localhost:8000.
Visit http://localhost:8000/docs for Swagger UI with interactive API docs.
```
---

### Features (update this as we go)
Frontend
Admin login using Firebase Google OAuth

Protected routes using React context and custom hooks

Dashboard displaying real-time API data

Styled with Tailwind CSS matching Podverse brand


Backend
FastAPI with asynchronous endpoints

OpenAPI docs fully integrated and customized

SQLite database with realistic dummy data for users, podcasts, episodes, stats

Pagination and filtering on list endpoints

JWT token verification via Firebase for secured routes (optional)



Environment Variables
Copy .env.example to .env.local (frontend) and .env (backend) and fill in:

Firebase API keys and OAuth info

Database URL (defaults to SQLite file)

Admin emails for access control (frontend)

Testing
Use pytest for backend API unit and integration tests

Use React Testing Library for frontend components (optional)

Postman or Swagger UI for manual API testing



Next Steps
Integrate PostgreSQL or production-grade DB

Add more detailed analytics and reporting

Implement admin role management in Firebase

Enhance security and error handling

Containerize app using Docker for deployment update the dockerfile



