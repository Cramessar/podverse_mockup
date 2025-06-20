-- Migration to add missing columns to channel table
-- Based on comparison between current schema and init_db.sql

-- First, let's check if the domain types exist, if not create them
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'short_id_v2') THEN
        CREATE DOMAIN short_id_v2 AS VARCHAR(15);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'varchar_slug') THEN
        CREATE DOMAIN varchar_slug AS VARCHAR(100);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'varchar_normal') THEN
        CREATE DOMAIN varchar_normal AS VARCHAR(255);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'varchar_short') THEN
        CREATE DOMAIN varchar_short AS VARCHAR(50);
    END IF;
END
$$;

-- Add missing columns to channel table
ALTER TABLE channel 
ADD COLUMN IF NOT EXISTS slug varchar_slug,
ADD COLUMN IF NOT EXISTS podcast_guid UUID,
ADD COLUMN IF NOT EXISTS title varchar_normal,
ADD COLUMN IF NOT EXISTS sortable_title varchar_short,
ADD COLUMN IF NOT EXISTS medium_id INTEGER,
ADD COLUMN IF NOT EXISTS has_podcast_index_value BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS has_value_time_splits BOOLEAN DEFAULT FALSE;

-- Add foreign key constraint for medium_id if medium table exists
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'medium') THEN
        ALTER TABLE channel 
        ADD CONSTRAINT channel_medium_id_fkey 
        FOREIGN KEY (medium_id) REFERENCES medium(id);
    END IF;
END
$$;

-- Create indexes
CREATE UNIQUE INDEX IF NOT EXISTS channel_podcast_guid_unique ON channel(podcast_guid) WHERE podcast_guid IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS channel_slug ON channel(slug) WHERE slug IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_channel_medium_id ON channel(medium_id); 