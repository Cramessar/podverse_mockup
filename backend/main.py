from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

from .routes import router as api_router

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)  # Disable default docs

app.include_router(api_router, prefix="/admin")

# Fix the openapi.yaml path for flat structure
# Change this if we change to a modular folder structure
OPENAPI_PATH = Path(__file__).parent / "openapi.yaml"

@app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    return FileResponse(OPENAPI_PATH)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.yaml",
        title="Podverse Admin API Docs",
        oauth2_redirect_url=None,
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    )

@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return HTMLResponse(get_swagger_ui_oauth2_redirect_html())


@app.get("/")
async def root():
    return {"message": "Podverse Admin API is running"}
