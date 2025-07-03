-- ai/db/db_init.sql

-- Drop existing tables if needed (be careful in prod!)
DROP TABLE IF EXISTS ai_channel_profiles CASCADE;
DROP TABLE IF EXISTS synced_entities CASCADE;

-- Table for synced raw data from backend endpoints
CREATE TABLE synced_entities (
    id SERIAL PRIMARY KEY,
    route_name VARCHAR(255),                
    entity_type VARCHAR(255) NOT NULL,      -- e.g. "channels", "feeds", more later
    url VARCHAR(512) NOT NULL,              -- full synced URL
    raw_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for structured AI-generated channel profiles
CREATE TABLE ai_channel_profiles (
    id SERIAL PRIMARY KEY,
    source_id INTEGER NOT NULL UNIQUE,      -- maps to backend entity ID
    title VARCHAR,
    slug VARCHAR,
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
