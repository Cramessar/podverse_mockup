
# Podverse Backend

Quick Flask app for managing podcasts and feeds. Uses a simple MVC pattern with some service layer stuff thrown in.

## Structure

```
backend/
├── app/
│   ├── models/podcast.py          # Database models (M)
│   ├── blueprints/podcast/
│   │   ├── routes.py              # API endpoints (Controller)
│   │   ├── services.py            # Business logic - Factory Pattern Service Layer
│   │   └── schemas.py             # JSON serialization (View)
│   ├── utils/                     # Utilities
│   └── __init__.py                # Flask app setup
├── manage.py                      # Start the server - Entry point (port 8000)
├── wsgi.py                        # Production deployment (future)
└── config.py                      # App configuration
```


## What's in each folder

- **models/** - All the database stuff 
- **blueprints/** - API routes organized by feature 
- **utils/** - Helper functions and utilities
- **openapi/** - Swagger docs and API specifications
- **tests/** - Unit tests and test fixtures
- **scripts/** - Helper scripts for database setup and maintenance
- **instance/** - Local config files (not in git)

## Running it

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py
```

Server runs on http://localhost:8000

## API Endpoints

- `GET /admin/podcast` - List all podcasts
- More endpoints coming as we build them out

## Database

Uses SQLite for now (`podverse_dummy.db`). Models are pretty straightforward - podcast, episodes, categories, etc. Check the models folder for the actual schema.

## Notes

This is just the basic structure. We'll probably add authentication, proper error handling, and more endpoints as we go.