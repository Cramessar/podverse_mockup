# ai/backend/sync/blueprint_parser.py
import re
from pathlib import Path

def extract_blueprint_routes():
    """Extracts blueprint routes from the Podverse backend blueprint registry."""
    init_file_path = Path("/podverse_backend/blueprints/__init__.py")
    if not init_file_path.exists():
        raise FileNotFoundError(f"[❌] Could not find __init__.py at: {init_file_path}")

    with init_file_path.open("r") as f:
        content = f.read()

    # Still flexible pattern, but remember we're nested under /admin
    pattern = re.compile(r'register_blueprint\((\w+),\s*url_prefix=["\'](/[\w/-]+)["\']\)')
    matches = pattern.findall(content)

    # ✅ Prepend /admin since the whole group is mounted under it
    routes = {name: f"/admin{url}" for name, url in matches}
    print(f"[ROUTES FOUND] {routes}")
    return routes
