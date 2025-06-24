# 🧠 Podverse Backend

This backend powers the **Podverse** project and serves three primary roles in the overall system:

1. **Database Integration & Scripting**  
   It acts as the source of truth for the PostgreSQL database, providing table definitions, ORM models, and helper scripts for generating and seeding data.

2. **API Documentation**  
   It exposes a self-documented API using Swagger/OpenAPI to make available endpoints easy to explore, test, and debug.

3. **Frontend-Ready Endpoints**  
   It provides well-structured, modular API endpoints intended for direct consumption by the React frontend, enabling seamless data interaction across views like dashboard analytics, podcast listings, and more.

Built with Flask, SQLAlchemy, and modular blueprints, this backend forms the core infrastructure for Podverse’s data and logic layer.

---

## 🚀 Tech Stack

- **Python 3.10+**
- **Flask** – Lightweight web framework for building RESTful APIs
- **SQLAlchemy** – ORM for defining models and managing database interactions
- **Flask-Migrate** – Alembic-based database migration support
- **FastAPI TestClient** – For lightweight and fast endpoint testing
- **PostgreSQL** – Production-ready database (orchestrated via Docker)
- **SQLite** – Local dev/testing fallback (`podverse_dummy.db`)
- **Docker** – Used to containerize the backend and manage dependencies in dev environments
- **Faker** – For generating mock data and seeding the database
- **OpenAPI / Swagger** – Interactive, auto-generated API documentation

---

## 📁 Folder Structure

```bash
backend/
├── app/
│   ├── __init__.py               # Flask app factory
│   ├── extensions.py             # Initializes db, migration, etc.
│   ├── models/                   # SQLAlchemy models (Channel, Feed, etc.)
│   ├── blueprints/               # Feature-based API route modules
│   ├── utils/                    # Shared utility functions
├── scripts/
│   ├── generate_dummy_users.py   # Faker-powered mock data seeder
│   ├── test_admin_api.py         # Tests for admin endpoints
│   ├── test_feed_insert.py       # Verifies feed DB interaction
│   └── ...                       # Any future scripts should go here
├── config.py                     # App environment configs (dev, prod, test)
├── main.py                       # App entry point
├── entrypoint.sh                 # Startup script for Docker (waits for DB, runs setup)
├── requirements.txt              # Python package dependencies
└── podverse_dummy.db             # Local SQLite fallback DB
```

📌 **Note:** Any standalone scripts—whether for testing, seeding, data migration, or debugging—should be placed in the `scripts/` folder.

---

## ⚙️ Configuration

App settings are defined in `config.py` and loaded based on the environment. The backend currently supports:

- **`DevelopmentConfig`** – Default config using SQLite and debug mode for local development.
- **`ProductionConfig`** – Placeholder for production-ready PostgreSQL deployments.
- **`TestingConfig`** – Placeholder for isolated testing environments.

The active config is selected in `main.py`:

```python
app = create_app('DevelopmentConfig')
```

---

### 🛠️ Docker Entrypoint

If you're running the app inside a container, the startup logic is handled by `entrypoint.sh`:

```bash
entrypoint.sh
├─ Waits for the PostgreSQL container to be ready
├─ Runs any setup scripts (like data seeding)
└─ Starts the Flask app
```

> 🧩 **Want to run something at container startup?**  
> Add it to `entrypoint.sh`.

#### 🔄 Line Endings Matter

Make sure `entrypoint.sh` uses **LF** (Unix) line endings—not CRLF (Windows)—or the container may fail to execute it.

To convert:

- **VS Code**: Click the "CRLF" in the bottom right and select **LF**
- **Terminal**:

  ```bash
  dos2unix entrypoint.sh
  ```

---

## 🐳 Running the Backend (Docker-First Approach)

The backend is designed to run inside a Docker container for consistency, portability, and smooth integration with the full-stack environment.

### 🔧 Quick Start

```bash
docker-compose up --build
```

This will:

- Build the backend image using `Dockerfile.backend`
- Wait for PostgreSQL to become available
- Run `scripts/generate_dummy_users.py` to seed the database
- Launch the Flask server in a container

📍 The API will be available at: **http://localhost:8000**

---

### 🧱 docker-compose.yml

```yaml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:5000"
    depends_on:
      - database
    environment:
      - FLASK_ENV=development
    volumes:
      - ./backend:/app
    command: sh entrypoint.sh

  database:
    image: postgres:13
    environment:
      POSTGRES_USER: podverse_admin
      POSTGRES_PASSWORD: testest
      POSTGRES_DB: podverse_db
    ports:
      - "5432:5432"
```

---

### 🧱 Dockerfile.backend

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY ./backend /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

EXPOSE 5000
CMD ["sh", "entrypoint.sh"]
```

---

## 📊 API Documentation & Endpoints

Once the backend is running, API documentation is available via Swagger UI.

### 🧭 Access Points

| URL                              | Description                            |
|----------------------------------|----------------------------------------|
| http://localhost:8000/docs       | Interactive Swagger UI (auto-generated) |
| http://localhost:8000/openapi.yaml | Raw OpenAPI spec for integration     |
| http://localhost:8000/           | Basic health check                    |

### 📬 Key Endpoints

| Method | Endpoint                             | Description                              |
|--------|--------------------------------------|------------------------------------------|
| GET    | /admin/dashboard                     | Returns site-wide stats (users, uptime)  |
| GET    | /admin/users                         | Lists all registered users               |
| GET    | /admin/podcasts                      | Lists available podcast records          |
| GET    | /admin/stats/listening-trends        | Returns date-based listening stats       |
| GET    | /admin/site-uptime                   | Provides uptime tracking info            |

> ✅ These endpoints are covered in `scripts/test_admin_api.py`

---

## 🧱 Database

- **Dev DB**: Uses SQLite by default (`podverse_dummy.db`) for fast local testing
- **Prod/Test DB**: Uses PostgreSQL via Docker

### 📦 Models

Located in `app/models/`, core entities include:

- `Channel`, `Feed`, `User`
- `FeedFlagStatus`, `StatsTrack*`, and other tracking tables

### 🌱 Seeding

Seed data is generated with:

```bash
scripts/generate_dummy_users.py
```

This runs automatically on container startup, or manually as needed.

---

## 🛣️ Roadmap

### ✅ Completed

- [x] Flask backend with modular blueprints
- [x] PostgreSQL + SQLite support
- [x] Swagger/OpenAPI documentation
- [x] Docker containerization
- [x] Analytics API endpoints
- [x] Faker-based data seeding

### 🛠️ In Progress

- [ ] Podcast feed ingestion expansion
- [ ] Improved test coverage
- [ ] Better error formatting and response handling
- [ ] Backend system monitoring
- [ ] Background task visibility and uptime tracking

### 🧠 Planned

- [ ] Full feed parsing pipeline
- [ ] Support for additional models (tags, categories, etc.)
- [ ] Background job queue integration (e.g., Celery)
- [ ] API versioning and rate limiting

For any questions please reach out to Daniel, Elif, or Garret 
