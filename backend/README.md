# Podverse Backend

Flask-based REST API for the Podverse podcast platform with PostgreSQL database and OpenAPI documentation.

## Tech Stack

- **Python 3.10+** with Flask
- **SQLAlchemy** ORM with PostgreSQL 
- **OpenAPI/Swagger** documentation
- **Docker** containerization
- **pytest** for testing
- **Celery + Redis** for background jobs

## Quick Start

### Using Docker (Recommended)

```bash
# From project root
docker-compose up --build
```

The backend service will:
- Run Flask API server on port 8000
- Auto-seed database with podcast dummy data  
- Start Celery worker for background tasks
- Connect to Redis for task queue management
- API available at: http://localhost:8000

> See main project README for complete Docker setup including all services.

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
│   │   ├── docs/            # Swagger UI routes
│   │   ├──health/           # Health check routes
│   │   ├──site/             # Site admin routes
│   ├── models/              # SQLAlchemy models (account, channel, feed, etc.)
│   ├── services/            # Shared, global services (feed parsing, data export)
│   ├── tasks/               # Celery background tasks (feed parsing, exports)
│   ├── templates/           # HTML templates (e.g., SQL runner)
│   ├── utils/               # Logging, auth, helpers
│   └── __init__.py          # Flask app factory 
├── scripts/                 # Data seeding scripts
├── tests/                   # pytest test files
├── openapi/                 # OpenAPI/Swagger specification 
├── instance/                # Local SQLite for local dev (optional)
├── config.py                # Environment configurations
├── main.py                  # Application entry point
├── make_celery.py           # Celery app factory and beat schedule
└── requirements.txt         # Python dependencies
```

## Domain Layout

| Layer          | Purpose                                                |
| -------------- | -------------------------------------------------------|
| **Route**      | Maps URL + method → controller                         |
| **Controller** | Handles input/output, talks to service                 |
| **Service**    | Domain specific business logic, DB actions             |
| **Schema**     | Validation + serialization                             |


## Environment Configuration

Set `FLASK_ENV` environment variable:
- `development` (default)
- `testing` 
- `production`

### Environment Variables

Create your `.env` file from the example:

```bash
cp backend/.env.example backend/.env
```

> These are automatically set in `docker-compose.yml` for containerized deployment.

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

