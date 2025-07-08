# ai/backend/utils/ensure_schema.py

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from ai.backend.db import engine  # ✅ Correct engine import


def column_exists(table_name, column_name):
    inspector = inspect(engine)
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    return column_name in columns


def table_exists(table_name):
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def add_missing_columns():
    if not table_exists("ai_channel_profiles"):
        print("[⚠️] Table 'ai_channel_profiles' does not exist — skipping column check.")
        return

    expected_columns = {
        "publisher": "TEXT",
        "feed_url": "TEXT",
        "medium_id": "INTEGER",
        "has_value_time_splits": "BOOLEAN",
        "has_podcast_index_value": "BOOLEAN",
        "raw_data": "JSONB"
    }

    for column, column_type in expected_columns.items():
        if not column_exists("ai_channel_profiles", column):
            print(f"[🛠️] Adding missing column: {column}")
            try:
                with engine.begin() as connection:
                    alter_sql = text(f"ALTER TABLE ai_channel_profiles ADD COLUMN {column} {column_type}")
                    connection.execute(alter_sql)
                print(f"[✅] Added column: {column}")
            except SQLAlchemyError as e:
                print(f"[❌] Failed to add column '{column}': {e}")
        else:
            print(f"[✔️] Column '{column}' already exists.")


def add_missing_tables():
    if not table_exists("synced_entities"):
        print("[🛠️] Creating missing table: synced_entities")
        create_sql = text("""
            CREATE TABLE synced_entities (
                id SERIAL PRIMARY KEY,
                route_name TEXT,
                synced_at TIMESTAMP DEFAULT NOW(),
                entity_type TEXT,
                entity_id INTEGER,
                raw_json JSONB
            )
        """)
        try:
            with engine.begin() as connection:
                connection.execute(create_sql)
            print("[✅] Table 'synced_entities' created.")
        except SQLAlchemyError as e:
            print(f"[❌] Failed to create 'synced_entities': {e}")
    else:
        print("[👌] Table 'synced_entities' already exists.")
