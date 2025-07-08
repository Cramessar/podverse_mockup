# Podverse Backend

Flask-based REST API for the Podverse podcast platform with PostgreSQL database and OpenAPI documentation.

## Tech Stack

- **Python 3.10+** with Flask
- **SQLAlchemy** ORM with PostgreSQL 
- **OpenAPI/Swagger** documentation
- **Docker** containerization
- **pytest** for testing

## Quick Start

### Using Docker (Recommended)

```bash
# From project root
docker-compose up --build
```

This will:
- Start PostgreSQL database
- Build and run the backend on port 8000
- Auto-seed database with dummy data
- API available at: http://localhost:8000

### Local Development

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python3 main.py
```

**Note:** Requires PostgreSQL running locally or update `DATABASE_URL` in config.

## API Documentation

- **Swagger UI**: http://localhost:8000/admin/docs
- **Health Check**: http://localhost:8000/health
- **SQL Runner**: http://localhost:8000/sql-runner
- **Admin Status**: http://localhost:8000/admin - Admin API status check
- **OpenAPI Specification**: http://localhost:8000/admin/docs/openapi.yaml - Raw OpenAPI spec file

## Project Structure

```
backend/
├── app/
│   ├── blueprints/          # API route modules
│   │   ├── feed/            # RSS feed management
│   │   │   ├── routes.py    # API endpoints (Controller)
│   │   │   ├── services.py  # Business logic - Factory Pattern Service Layer
│   │   │   └── schemas.py   # JSON serialization (View)
│   │   ├── docs/            # Swagger UI routes
│   │   ├──health/          # Health check routes
        └── ..
│   ├── models/              # SQLAlchemy models (account, channel, feed, etc.)
│   ├── services/            # feed_parser.py - RSS parsing logic
│   ├── tasks/               # feed_task.py - Background tasks
│   ├── templates/           # sql_runner.html - SQL interface
│   ├── utils/               # logger.py, utils.py - Logging & utilities
│   └── __init__.py          # Flask app factory with CORS & logging
├── scripts/                 # generate_dummy_users.py - Data seeding
├── tests/                   # pytest test files
├── openapi/                 # OpenAPI/Swagger specification files
├── instance/                # podverse.db - SQLite for local dev
├── config.py                # Environment configurations
├── main.py                  # Application entry point
└── requirements.txt         # Python dependencies
```

## Environment Configuration

Set `FLASK_ENV` environment variable:
- `development` (default)
- `testing` 
- `production`

Database URL: `postgresql://podverse_admin:testest@database:5432/podverse_db`

## Available Endpoints

| Prefix | Description |
|--------|-------------|
| `/admin/channels` | Channel management |
| `/admin/feeds` | RSS feed operations |
| `/admin/items` | Episode/item management |
| `/admin/categories` | Category operations |
| `/admin/mediums` | Media type management |
| `/admin/stats` | Analytics and statistics |

## Testing

```bash
pytest tests/
```

## Logging

Centralized logging system with request/response tracking and security event logging.


| Layer          | Purpose                                |
| -------------- | -------------------------------------- |
| **Route**      | Maps URL + method → controller         |
| **Controller** | Handles input/output, talks to service |
| **Service**    | Business logic, DB actions             |
| **Schema**     | Validation + serialization             |
