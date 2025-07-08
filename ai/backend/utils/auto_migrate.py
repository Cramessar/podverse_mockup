# ai/backend/utils/auto_migrate.py

import logging
from sqlalchemy import inspect, text
from sqlalchemy.exc import ProgrammingError, OperationalError
from ai.backend.db import engine, Base

logger = logging.getLogger(__name__)


def add_missing_columns(engine, model):
    inspector = inspect(engine)
    table_name = model.__tablename__

    try:
        db_columns = {col["name"] for col in inspector.get_columns(table_name)}
    except Exception as e:
        logger.warning(f"[AutoMigrate] Could not inspect columns for table '{table_name}': {e}")
        return

    for col in model.__table__.columns:
        if col.name not in db_columns:
            col_type = str(col.type.compile(engine.dialect))
            nullable = "NULL" if col.nullable else "NOT NULL"
            default = f"DEFAULT {col.default.arg}" if col.default is not None else ""

            alter_stmt = f"""
                ALTER TABLE {table_name}
                ADD COLUMN {col.name} {col_type} {nullable} {default};
            """
            try:
                with engine.connect() as conn:
                    conn.execute(text(alter_stmt.strip()))
                logger.info(f"[AutoMigrate] Added column '{col.name}' to '{table_name}'")
            except (ProgrammingError, OperationalError) as e:
                logger.error(f"[AutoMigrate] Failed to add column '{col.name}' to '{table_name}': {e}")


def create_missing_tables():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            try:
                table.create(bind=engine)
                logger.info(f"[AutoMigrate] Created missing table '{table.name}'")
            except Exception as e:
                logger.error(f"[AutoMigrate] Failed to create table '{table.name}': {e}")


def auto_migrate():
    logger.info("[AutoMigrate] Starting schema check...")

    # Add missing tables
    create_missing_tables()

    # Add missing columns to existing tables
    for cls in Base.__subclasses__():
        try:
            add_missing_columns(engine, cls)
        except Exception as e:
            logger.error(f"[AutoMigrate] Failed to process model '{cls.__name__}': {e}")

    logger.info("[AutoMigrate] ✅ Schema auto-migration complete.")
