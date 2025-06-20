# OpenAPI Documentation

This folder contains all the API documentation and specifications for the Podverse backend.

## Structure

```
openapi/
├── openapi.yaml           # Main OpenAPI spec file  
├── bundled.yaml          # Single-file version (used by server)
├── paths/                # API endpoint definitions
│   ├── feeds.yaml       # Feed management endpoints
│   ├── channels.yaml    # Channel/podcast endpoints  
│   ├── items.yaml       # Episode/item endpoints
│   ├── categories.yaml  # Category endpoints
│   ├── mediums.yaml     # Media type endpoints
│   └── stats.yaml       # Statistics endpoints
└── components/          # Reusable OpenAPI components
    ├── schemas/         # Data models (Feed, Channel, Item, etc.)
    ├── parameters/      # Common query parameters (limit, offset, search)
    └── responses/       # Standard error responses
```

## Quick Commands after cd backend

**Validate the spec:**
```bash
npx @redocly/cli lint openapi/openapi.yaml
```
*Use this when making changes to check for errors*

**Bundle for server:**
```bash
npx @redocly/cli bundle openapi/openapi.yaml --output openapi/bundled.yaml
```
*Run this after making changes - server uses bundled.yaml*

**Generate docs:**
```bash
npx @redocly/cli build-docs openapi/openapi.yaml --output docs.html
```
*Creates standalone HTML documentation*

## Viewing the docs

- **Swagger UI**: http://localhost:8000/admin/docs/ 
- **Raw spec**: http://localhost:8000/admin/openapi.yaml

## Making changes

1. Edit files in `paths/` or `components/schemas/`
2. **Validate**: `npx @redocly/cli lint openapi/openapi.yaml`
3. **Bundle**: `npx @redocly/cli bundle openapi/openapi.yaml --output openapi/bundled.yaml`
4. Restart server or hard refresh browser
5. Check Swagger UI for your changes

## Key schemas match database tables:
- Feed → `feed` table
- Channel → `channel` table  
- Item → `item` table
- Category → `category` table
- Medium → `medium` table

**Always bundle after changes** - the server serves `bundled.yaml`, not `openapi.yaml`. 