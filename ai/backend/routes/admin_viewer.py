# ai/backend/routes/admin_viewer.py

from flask import Blueprint, render_template_string, request
from sqlalchemy import inspect
from ai.backend.db import SessionLocal
from ai.backend.models.synced_entity import SyncedEntity
from ai.backend.models.ai_profiles import AIChannelProfile

admin_viewer_bp = Blueprint("admin_viewer", __name__, url_prefix="/admin/db-viewer")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>📊 AI DB Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 2rem; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 0.9rem; }
        th { background-color: #f5f5f5; }
        h1, h2 { margin-top: 2rem; }
        select { padding: 5px 10px; font-size: 1rem; }
    </style>
</head>
<body>
    <h1>AI DB Viewer</h1>

    <form method="GET">
        <label for="table">Select table:</label>
        <select name="table" onchange="this.form.submit()">
            <option value="synced_entities" {% if table == 'synced_entities' %}selected{% endif %}>SyncedEntity</option>
            <option value="ai_channel_profiles" {% if table == 'ai_channel_profiles' %}selected{% endif %}>AIChannelProfile</option>
        </select>
    </form>

    <h2>Preview: {{ table }}</h2>
    {% if rows %}
    <table>
        <thead>
            <tr>
                {% for col in columns %}
                    <th>{{ col }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
                <tr>
                    {% for col in columns %}
                        <td>{{ row[col] }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
        <p>No data found in {{ table }}</p>
    {% endif %}
</body>
</html>
"""

@admin_viewer_bp.route("/", methods=["GET"])
def db_viewer():
    session = SessionLocal()
    table = request.args.get("table", "synced_entities")

    data = []
    columns = []

    try:
        if table == "synced_entities":
            rows = session.query(SyncedEntity).order_by(SyncedEntity.id.desc()).limit(25).all()
        elif table == "ai_channel_profiles":
            rows = session.query(AIChannelProfile).order_by(AIChannelProfile.id.desc()).limit(25).all()
        else:
            rows = []

        if rows:
            columns = rows[0].__table__.columns.keys()
            data = [row.__dict__ for row in rows]
            for d in data:
                d.pop("_sa_instance_state", None)

    except Exception as e:
        print(f"[Viewer Error] {e}")
    finally:
        session.close()

    return render_template_string(HTML_TEMPLATE, table=table, rows=data, columns=columns)
