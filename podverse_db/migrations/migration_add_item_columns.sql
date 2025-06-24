-- Migration to add missing columns to item table
-- Based on comparison between current schema and init_db.sql

-- First, create the item_flag_status table if it doesn't exist
CREATE TABLE IF NOT EXISTS item_flag_status (
    id SERIAL PRIMARY KEY,
    status TEXT UNIQUE CHECK (status IN ('active', 'pending-archive', 'archived', 'pending-delete')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert default statuses if they don't exist
INSERT INTO item_flag_status (status) VALUES ('active'), ('pending-archive'), ('archived'), ('pending-delete')
ON CONFLICT (status) DO NOTHING;

-- Add missing columns to item table
ALTER TABLE item 
ADD COLUMN IF NOT EXISTS slug varchar_slug,
ADD COLUMN IF NOT EXISTS guid VARCHAR(2083),
ADD COLUMN IF NOT EXISTS guid_enclosure_url VARCHAR(2083),
ADD COLUMN IF NOT EXISTS pub_date TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS title VARCHAR(255),
ADD COLUMN IF NOT EXISTS item_flag_status_id INTEGER;

-- Set default item_flag_status_id to 'active' status for existing records
UPDATE item 
SET item_flag_status_id = (SELECT id FROM item_flag_status WHERE status = 'active')
WHERE item_flag_status_id IS NULL;

-- Make item_flag_status_id NOT NULL after setting defaults
ALTER TABLE item 
ALTER COLUMN item_flag_status_id SET NOT NULL;

-- Add foreign key constraint for item_flag_status_id
ALTER TABLE item 
ADD CONSTRAINT item_item_flag_status_id_fkey 
FOREIGN KEY (item_flag_status_id) REFERENCES item_flag_status(id);

-- Add check constraint to ensure either guid or guid_enclosure_url is present
ALTER TABLE item 
ADD CONSTRAINT item_guid_check 
CHECK (guid IS NOT NULL OR guid_enclosure_url IS NOT NULL);

-- Create indexes
CREATE UNIQUE INDEX IF NOT EXISTS item_slug ON item(slug) WHERE slug IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_item_guid ON item(guid);
CREATE INDEX IF NOT EXISTS idx_item_guid_enclosure_url ON item(guid_enclosure_url);
CREATE INDEX IF NOT EXISTS idx_item_item_flag_status_id ON item(item_flag_status_id); 