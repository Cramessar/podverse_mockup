-- Migration: Add parse_error and fetch_error to feed_flag_status

-- Drop the existing constraint
ALTER TABLE feed_flag_status 
DROP CONSTRAINT feed_flag_status_status_check;

-- Add the updated constraint with new values
ALTER TABLE feed_flag_status 
ADD CONSTRAINT feed_flag_status_status_check 
CHECK (status IN ('active', 'always-parse', 'spam', 'pending-archive', 'archived', 'takedown', 'parse_error', 'fetch_error'));

-- Insert the new status values
INSERT INTO feed_flag_status (status) VALUES ('parse_error'), ('fetch_error'); 