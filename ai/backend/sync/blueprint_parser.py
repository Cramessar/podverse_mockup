# ai/backend/sync/blueprint_parser.py

import re
from pathlib import Path
import os

def extract_blueprint_routes():
    """Extracts blueprint routes from the Podverse backend blueprint registry."""
    
    # ✅ Fallback to correct backend location inside AI container
    base_path = os.getenv("PODVERSE_BACKEND_PATH", "/app/backend/app")
    init_file_path = Path(base_path) / "blueprints" / "__init__.py"

    print(f"[🔍] Looking for __init__.py at: {init_file_path}")

    if not init_file_path.exists():
        raise FileNotFoundError(f"[❌] Could not find __init__.py at: {init_file_path}")

    with init_file_path.open("r") as f:
        content = f.read()

    pattern = re.compile(r'register_blueprint\((\w+),\s*url_prefix=["\'](/[\w/-]+)["\']\)')
    matches = pattern.findall(content)

    routes = {name: f"/admin{url}" for name, url in matches}
    print(f"[✅ ROUTES FOUND] {routes}")
    return routes
