
# Podverse Backend

Quick Flask app for managing channels and feeds. Uses a simple MVC pattern with some service layer stuff thrown in.

## Structure

```
backend/
├── app/
│   ├── models/channel.py          # Database models (M)
│   ├── blueprints/channel/
│   │   ├── routes.py              # API endpoints (Controller)
│   │   ├── services.py            # Business logic - Factory Pattern Service Layer
│   │   └── schemas.py             # JSON serialization (View)
│   ├── utils/                     # Utilities
│   └── __init__.py                # Flask app setup
├── main.py                        # Start the server - Entry point (port 8000)
└── config.py                      # App configuration
```


## What's in each folder

- **models/** - All the database stuff (channel.py, channel_category.py, category.py, feed.py, etc.)
- **blueprints/** - API routes organized by feature (channel, docs, item) 
- **utils/** - Helper functions and utilities
- **openapi/** - Swagger docs and API specifications
- **tests/** - Unit tests and test fixtures
- **scripts/** - Helper scripts for database setup and maintenance
- **instance/** - Local config files (not in git)

## Running it

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python3 main.py
```

Server runs on http://localhost:8000

## Access Points

- **API Documentation**: http://localhost:8000/docs - Interactive Swagger UI
- **Admin Documentation**: http://localhost:8000/admin/docs - Alternative admin docs route  
- **OpenAPI Specification**: http://localhost:8000/openapi.yaml - Raw OpenAPI spec file 
- **API Status**: http://localhost:8000/ - Basic API health check

## API Endpoints

- `GET /admin/channel` - List all channels
- More endpoints coming as we build them out

## Database

Uses SQLite for now (`podverse_dummy.db`). Models are pretty straightforward - channel, episodes, categories, etc. Check the models folder for the actual schema.

## Notes

This is just the basic structure. We'll probably add authentication, proper error handling, and more endpoints as we go.