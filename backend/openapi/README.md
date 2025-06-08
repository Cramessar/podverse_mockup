# OpenAPI Documentation

This folder contains all the API documentation and specifications for the Podverse backend.

## Structure

```
openapi/
├── openapi.yaml           # Main OpenAPI spec file
├── paths/                # API endpoint definitions
│   ├── auth/            # Authentication endpoints
│   └── channel/         # Channel/podcast endpoints
└── components/          # Reusable OpenAPI components
    ├── schemas/         # Data models and request/response schemas
    └── responses/       # Common response definitions
```

## What's what

- **openapi.yaml** - The main spec file that ties everything together
- **paths/** - Each folder has the actual API endpoint definitions
- **components/** - Shared stuff like error responses and data models

## Using the docs

The OpenAPI spec gets served automatically when you run the backend. Check it out at:
- Swagger UI: http://localhost:8000/docs
- Raw spec: http://localhost:8000/openapi.yaml

## Adding new endpoints

1. Create/update files in `paths/` for your new endpoints
2. Add any new schemas to `components/schemas/`
3. Reference them in the main `openapi.yaml` file
4. Test it in the Swagger UI

Pretty standard OpenAPI 3.0 setup - nothing fancy. 