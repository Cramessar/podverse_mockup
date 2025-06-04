-- Enable extensions (if using PostgreSQL)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Accounts table with JSONB for profile/settings/memberships
CREATE TABLE account (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  profile JSONB DEFAULT '{}'::jsonb,           -- e.g., name, avatar, bio
  settings JSONB DEFAULT '{}'::jsonb,          -- notification preferences etc.
  memberships JSONB DEFAULT '[]'::jsonb        -- membership tiers, history
);

-- Podcasts (channels) with metadata in JSONB
CREATE TABLE podcast (
  id SERIAL PRIMARY KEY,
  title VARCHAR(512) NOT NULL,
  publisher VARCHAR(512),
  description TEXT,
  categories JSONB DEFAULT '[]'::jsonb,        -- category IDs/names
  feed_url VARCHAR(1024),
  metadata JSONB DEFAULT '{}'::jsonb,           -- images, licenses, etc.
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Episodes with metadata in JSONB
CREATE TABLE episode (
  id SERIAL PRIMARY KEY,
  podcast_id INT NOT NULL REFERENCES podcast(id) ON DELETE CASCADE,
  title VARCHAR(512) NOT NULL,
  description TEXT,
  pub_date TIMESTAMP WITH TIME ZONE,
  media JSONB DEFAULT '{}'::jsonb,              -- urls, duration, transcripts, chapters
  stats JSONB DEFAULT '{}'::jsonb,              -- listens, ratings, etc.
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Feeds table for raw feed URLs and parsing info
CREATE TABLE feed (
  id SERIAL PRIMARY KEY,
  url VARCHAR(1024) UNIQUE NOT NULL,
  last_fetched TIMESTAMP WITH TIME ZONE,
  status VARCHAR(50),
  metadata JSONB DEFAULT '{}'::jsonb
);

-- Playlists with array of episode IDs and metadata
CREATE TABLE playlist (
  id SERIAL PRIMARY KEY,
  account_id INT NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  episode_ids INT[] DEFAULT '{}',               -- ordered list of episodes
  metadata JSONB DEFAULT '{}'::jsonb,           -- e.g., created_at, privacy settings
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Subscriptions table: tracks what users follow (podcasts, accounts, etc.)
CREATE TABLE subscription (
  id SERIAL PRIMARY KEY,
  account_id INT NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  target_type VARCHAR(50) NOT NULL,             -- e.g., 'podcast', 'account'
  target_id INT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE(account_id, target_type, target_id)
);

-- Aggregated stats for various entities
CREATE TABLE stats (
  id SERIAL PRIMARY KEY,
  entity_type VARCHAR(50) NOT NULL,             -- e.g., 'podcast', 'episode', 'account'
  entity_id INT NOT NULL,
  stat_date DATE NOT NULL,
  listens INT DEFAULT 0,
  downloads INT DEFAULT 0,
  rating FLOAT DEFAULT 0,
  UNIQUE(entity_type, entity_id, stat_date)
);

-- Media table for clips, soundbites, etc.
CREATE TABLE media (
  id SERIAL PRIMARY KEY,
  episode_id INT REFERENCES episode(id) ON DELETE CASCADE,
  media_type VARCHAR(50),                        -- e.g., 'clip', 'soundbite'
  url VARCHAR(1024) NOT NULL,
  duration INT,                                  -- seconds
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Notifications/preferences for users stored as JSONB
CREATE TABLE notifications (
  id SERIAL PRIMARY KEY,
  account_id INT NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  preferences JSONB DEFAULT '{}'::jsonb,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Indexes for performance
CREATE INDEX idx_podcast_categories ON podcast USING GIN (categories);
CREATE INDEX idx_episode_podcast_id ON episode (podcast_id);
CREATE INDEX idx_subscription_account ON subscription (account_id);
CREATE INDEX idx_stats_entity ON stats (entity_type, entity_id, stat_date);
CREATE INDEX idx_media_episode_id ON media (episode_id);
CREATE INDEX idx_notifications_account ON notifications (account_id);

