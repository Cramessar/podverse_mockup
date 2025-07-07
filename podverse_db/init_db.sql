-- 0000 migration

-- Helpers

-- START CREATE read AND read_write users

-- Create the "read" user if it doesn't already exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'read') THEN
        CREATE USER read WITH PASSWORD 'your_read_password';
    END IF;
END
$$;

-- Create the "read_write" user if it doesn't already exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'read_write') THEN
        CREATE USER read_write WITH PASSWORD 'your_read_write_password';
    END IF;
END
$$;

-- Grant CONNECT and USAGE privileges on the database and schema to both users
GRANT CONNECT ON DATABASE postgres TO read, read_write;
GRANT USAGE ON SCHEMA public TO read, read_write;

-- Grant SELECT privileges on all tables and sequences to the "read" user
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO read;

-- Grant SELECT, INSERT, UPDATE, DELETE privileges on all tables to the "read_write" user
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO read_write;
GRANT SELECT, USAGE, UPDATE ON ALL SEQUENCES IN SCHEMA public TO read_write;

-- Ensure future tables and sequences have the correct privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON SEQUENCES TO read;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO read_write;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, USAGE, UPDATE ON SEQUENCES TO read_write;

-- END CREATE read AND read_write users


-- DOMAIN DEFINITIONS --
CREATE DOMAIN short_id_v2 AS VARCHAR(64);
CREATE DOMAIN varchar_short AS VARCHAR(50);
CREATE DOMAIN varchar_normal AS VARCHAR(255);
CREATE DOMAIN varchar_md5 AS VARCHAR(64);
CREATE DOMAIN varchar_slug AS VARCHAR(100);
CREATE DOMAIN varchar_uri AS VARCHAR(2083);
CREATE DOMAIN varchar_url AS VARCHAR(2083) CHECK (VALUE ~ '^https?://|^http?://');
CREATE DOMAIN server_time AS TIMESTAMP;
CREATE DOMAIN server_time_with_default AS TIMESTAMP DEFAULT NOW();

-- Function to set updated_at
CREATE OR REPLACE FUNCTION set_updated_at_field()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 0001 migration

/*

PODVERSE ADMIN DATABASE SCHEMA

- The `id` column is a SERIAL column that is used as the primary key for every table.

- The `id_text` column is only intended for tables where the data is available as urls.
  For example, https://podverse.fm/podcast/abc123def456, the `id_text` column would be `abc123def456`.

- The `slug` column is not required, but functions as an alternative for `id_text`.
  For example, https://podverse.fm/podcast/podcasting-20 would have a `slug` column with the value `podcasting-20`.

- The `podcast_index_id` ensures that our database only contains feed data that is available in the Podcast Index API.

*/

----------** GLOBAL REFERENCE TABLES **----------
-- These tables are referenced across many tables, and must be created first.

--** CATEGORY

-- Allowed category values align with the standard categories and subcategories
-- supported by Apple iTunes through the <itunes:category> tag.
-- 
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES category(id) ON DELETE CASCADE,
    display_name varchar_normal NOT NULL, -- our own display name for the category
    slug varchar_normal NOT NULL, -- our own web url slug for the category
    mapping_key varchar_normal NOT NULL -- camel case version of the slug
);

CREATE INDEX idx_category_parent_id ON category(parent_id);

-- Insert parent categories
INSERT INTO category (parent_id, display_name, slug, mapping_key) VALUES
(NULL, 'Arts', 'arts', 'arts'),
(NULL, 'Business', 'business', 'business'),
(NULL, 'Comedy', 'comedy', 'comedy'),
(NULL, 'Education', 'education', 'education'),
(NULL, 'Fiction', 'fiction', 'fiction'),
(NULL, 'Government', 'government', 'government'),
(NULL, 'History', 'history', 'history'),
(NULL, 'Health & Fitness', 'health-and-fitness', 'healthandfitness'),
(NULL, 'Kids & Family', 'kids-and-family', 'kidsandfamily'),
(NULL, 'Leisure', 'leisure', 'leisure'),
(NULL, 'Music', 'music', 'music'),
(NULL, 'News', 'news', 'news'),
(NULL, 'Religion & Spirituality', 'religion-and-spirituality', 'religionandspirituality'),
(NULL, 'Science', 'science', 'science'),
(NULL, 'Society & Culture', 'society-and-culture', 'societyandculture'),
(NULL, 'Sports', 'sports', 'sports'),
(NULL, 'Technology', 'technology', 'technology'),
(NULL, 'True Crime', 'true-crime', 'truecrime'),
(NULL, 'TV & Film', 'tv-and-film', 'tvandfilm');

-- Insert child categories
INSERT INTO category (parent_id, display_name, slug, mapping_key) VALUES
((SELECT id FROM category WHERE display_name = 'Arts'), 'Books', 'books', 'books'),
((SELECT id FROM category WHERE display_name = 'Arts'), 'Design', 'design', 'design'),
((SELECT id FROM category WHERE display_name = 'Arts'), 'Fashion & Beauty', 'fashion-and-beauty', 'fashionandbeauty'),
((SELECT id FROM category WHERE display_name = 'Arts'), 'Food', 'food', 'food'),
((SELECT id FROM category WHERE display_name = 'Arts'), 'Performing Arts', 'performing-arts', 'performingarts'),
((SELECT id FROM category WHERE display_name = 'Arts'), 'Visual Arts', 'visual-arts', 'visualarts'),
((SELECT id FROM category WHERE display_name = 'Business'), 'Careers', 'careers', 'careers'),
((SELECT id FROM category WHERE display_name = 'Business'), 'Entrepreneurship', 'entrepreneurship', 'entrepreneurship'),
((SELECT id FROM category WHERE display_name = 'Business'), 'Investing', 'investing', 'investing'),
((SELECT id FROM category WHERE display_name = 'Business'), 'Management', 'management', 'management'),
((SELECT id FROM category WHERE display_name = 'Business'), 'Marketing', 'marketing', 'marketing'),
((SELECT id FROM category WHERE display_name = 'Business'), 'Non-Profit', 'non-profit', 'nonprofit'),
((SELECT id FROM category WHERE display_name = 'Comedy'), 'Comedy Interviews', 'comedy-interviews', 'comedyinterviews'),
((SELECT id FROM category WHERE display_name = 'Comedy'), 'Improv', 'improv', 'improv'),
((SELECT id FROM category WHERE display_name = 'Comedy'), 'Stand-Up', 'stand-up', 'standup'),
((SELECT id FROM category WHERE display_name = 'Education'), 'Courses', 'courses', 'courses'),
((SELECT id FROM category WHERE display_name = 'Education'), 'How To', 'how-to', 'howto'),
((SELECT id FROM category WHERE display_name = 'Education'), 'Language Learning', 'language-learning', 'languagelearning'),
((SELECT id FROM category WHERE display_name = 'Education'), 'Self-Improvement', 'self-improvement', 'selfimprovement'),
((SELECT id FROM category WHERE display_name = 'Fiction'), 'Comedy Fiction', 'comedy-fiction', 'comedyfiction'),
((SELECT id FROM category WHERE display_name = 'Fiction'), 'Drama', 'drama', 'drama'),
((SELECT id FROM category WHERE display_name = 'Fiction'), 'Science Fiction', 'science-fiction', 'sciencefiction'),
((SELECT id FROM category WHERE display_name = 'Health & Fitness'), 'Alternative Health', 'alternative-health', 'alternativehealth'),
((SELECT id FROM category WHERE display_name = 'Health & Fitness'), 'Fitness', 'fitness', 'fitness'),
((SELECT id FROM category WHERE display_name = 'Health & Fitness'), 'Medicine', 'medicine', 'medicine'),
((SELECT id FROM category WHERE display_name = 'Health & Fitness'), 'Mental Health', 'mental-health', 'mentalhealth'),
((SELECT id FROM category WHERE display_name = 'Health & Fitness'), 'Nutrition', 'nutrition', 'nutrition'),
((SELECT id FROM category WHERE display_name = 'Health & Fitness'), 'Sexuality', 'sexuality', 'sexuality'),
((SELECT id FROM category WHERE display_name = 'Kids & Family'), 'Education for Kids', 'education-for-kids', 'educationforkids'),
((SELECT id FROM category WHERE display_name = 'Kids & Family'), 'Parenting', 'parenting', 'parenting'),
((SELECT id FROM category WHERE display_name = 'Kids & Family'), 'Pets & Animals', 'pets-and-animals', 'petsandanimals'),
((SELECT id FROM category WHERE display_name = 'Kids & Family'), 'Stories for Kids', 'stories-for-kids', 'storiesforkids'),
((SELECT id FROM category WHERE display_name = 'Leisure'), 'Animation & Manga', 'animation-and-manga', 'animationandmanga'),
((SELECT id FROM category WHERE display_name = 'Leisure'), 'Automotive', 'automotive', 'automotive'),
((SELECT id FROM category WHERE display_name = 'Leisure'), 'Aviation', 'aviation', 'aviation'),
((SELECT id FROM category WHERE display_name = 'Leisure'), 'Crafts', 'crafts', 'crafts'),
((SELECT id FROM category WHERE display_name = 'Leisure'), 'Games', 'games', 'games'),
((SELECT id FROM category WHERE display_name = 'Leisure'), 'Hobbies', 'hobbies', 'hobbies'),
((SELECT id FROM category WHERE display_name = 'Leisure'), 'Home & Garden', 'home-and-garden', 'homeandgarden'),
((SELECT id FROM category WHERE display_name = 'Leisure'), 'Video Games', 'video-games', 'videogames'),
((SELECT id FROM category WHERE display_name = 'Music'), 'Music Commentary', 'music-commentary', 'musiccommentary'),
((SELECT id FROM category WHERE display_name = 'Music'), 'Music History', 'music-history', 'musichistory'),
((SELECT id FROM category WHERE display_name = 'Music'), 'Music Interviews', 'music-interviews', 'musicinterviews'),
((SELECT id FROM category WHERE display_name = 'News'), 'Business News', 'business-news', 'businessnews'),
((SELECT id FROM category WHERE display_name = 'News'), 'Daily News', 'daily-news', 'dailynews'),
((SELECT id FROM category WHERE display_name = 'News'), 'Entertainment News', 'entertainment-news', 'entertainmentnews'),
((SELECT id FROM category WHERE display_name = 'News'), 'News Commentary', 'news-commentary', 'newscommentary'),
((SELECT id FROM category WHERE display_name = 'News'), 'Politics', 'politics', 'politics'),
((SELECT id FROM category WHERE display_name = 'News'), 'Sports News', 'sports-news', 'sportsnews'),
((SELECT id FROM category WHERE display_name = 'News'), 'Tech News', 'tech-news', 'technews'),
((SELECT id FROM category WHERE display_name = 'Religion & Spirituality'), 'Buddhism', 'buddhism', 'buddhism'),
((SELECT id FROM category WHERE display_name = 'Religion & Spirituality'), 'Christianity', 'christianity', 'christianity'),
((SELECT id FROM category WHERE display_name = 'Religion & Spirituality'), 'Hinduism', 'hinduism', 'hinduism'),
((SELECT id FROM category WHERE display_name = 'Religion & Spirituality'), 'Islam', 'islam', 'islam'),
((SELECT id FROM category WHERE display_name = 'Religion & Spirituality'), 'Judaism', 'judaism', 'judaism'),
((SELECT id FROM category WHERE display_name = 'Religion & Spirituality'), 'Religion', 'religion', 'religion'),
((SELECT id FROM category WHERE display_name = 'Religion & Spirituality'), 'Spirituality', 'spirituality', 'spirituality'),
((SELECT id FROM category WHERE display_name = 'Science'), 'Astronomy', 'astronomy', 'astronomy'),
((SELECT id FROM category WHERE display_name = 'Science'), 'Chemistry', 'chemistry', 'chemistry'),
((SELECT id FROM category WHERE display_name = 'Science'), 'Earth Sciences', 'earth-sciences', 'earthsciences'),
((SELECT id FROM category WHERE display_name = 'Science'), 'Life Sciences', 'life-sciences', 'lifesciences'),
((SELECT id FROM category WHERE display_name = 'Science'), 'Mathematics', 'mathematics', 'mathematics'),
((SELECT id FROM category WHERE display_name = 'Science'), 'Natural Sciences', 'natural-sciences', 'naturalsciences'),
((SELECT id FROM category WHERE display_name = 'Science'), 'Nature', 'nature', 'nature'),
((SELECT id FROM category WHERE display_name = 'Science'), 'Physics', 'physics', 'physics'),
((SELECT id FROM category WHERE display_name = 'Science'), 'Social Sciences', 'social-sciences', 'socialsciences'),
((SELECT id FROM category WHERE display_name = 'Society & Culture'), 'Documentary', 'documentary', 'documentary'),
((SELECT id FROM category WHERE display_name = 'Society & Culture'), 'Personal Journals', 'personal-journals', 'personaljournals'),
((SELECT id FROM category WHERE display_name = 'Society & Culture'), 'Philosophy', 'philosophy', 'philosophy'),
((SELECT id FROM category WHERE display_name = 'Society & Culture'), 'Places & Travel', 'places-and-travel', 'placesandtravel'),
((SELECT id FROM category WHERE display_name = 'Society & Culture'), 'Relationships', 'relationships', 'relationships'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Baseball', 'baseball', 'baseball'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Basketball', 'basketball', 'basketball'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Cricket', 'cricket', 'cricket'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Fantasy Sports', 'fantasy-sports', 'fantasysports'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Football', 'football', 'football'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Golf', 'golf', 'golf'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Hockey', 'hockey', 'hockey'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Rugby', 'rugby', 'rugby'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Running', 'running', 'running'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Soccer', 'soccer', 'soccer'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Swimming', 'swimming', 'swimming'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Tennis', 'tennis', 'tennis'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Volleyball', 'volleyball', 'volleyball'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Wilderness', 'wilderness', 'wilderness'),
((SELECT id FROM category WHERE display_name = 'Sports'), 'Wrestling', 'wrestling', 'wrestling'),
((SELECT id FROM category WHERE display_name = 'TV & Film'), 'After Shows', 'after-shows', 'aftershows'),
((SELECT id FROM category WHERE display_name = 'TV & Film'), 'Film History', 'film-history', 'filmhistory'),
((SELECT id FROM category WHERE display_name = 'TV & Film'), 'Film Interviews', 'film-interviews', 'filminterviews'),
((SELECT id FROM category WHERE display_name = 'TV & Film'), 'Film Reviews', 'film-reviews', 'filmreviews'),
((SELECT id FROM category WHERE display_name = 'TV & Film'), 'TV Reviews', 'tv-reviews', 'tvreviews');

--** MEDIUM VALUE

-- <podcast:medium>
CREATE TABLE medium (
    id SERIAL PRIMARY KEY,
    value TEXT UNIQUE CHECK (VALUE IN (
        'publisher',
        'podcast', 'music', 'video', 'film', 'audiobook', 'newsletter', 'blog', 'publisher', 'course',
        'mixed', 'podcastL', 'musicL', 'videoL', 'filmL', 'audiobookL', 'newsletterL', 'blogL', 'publisherL', 'courseL'
    ))
);

INSERT INTO medium (value) VALUES
    ('publisher'),
    ('podcast'), ('music'), ('video'), ('film'), ('audiobook'), ('newsletter'), ('blog'), ('course'),
    ('mixed'), ('podcastL'), ('musicL'), ('videoL'), ('filmL'), ('audiobookL'), ('newsletterL'), ('blogL'), ('publisherL'), ('courseL')
;

----------** TABLES **----------

--** FEED > FLAG STATUS

-- used internally for identifying and handling spam and other special flag statuses.
CREATE TABLE feed_flag_status (
    id SERIAL PRIMARY KEY,
    status TEXT UNIQUE CHECK (status IN ('active', 'always-parse', 'spam', 'pending-archive', 'archived', 'takedown', 'parse_error', 'fetch_error')),
    created_at server_time_with_default,
    updated_at server_time_with_default
);

CREATE TRIGGER set_updated_at_feed_flag_status
BEFORE UPDATE ON feed_flag_status
FOR EACH ROW
EXECUTE FUNCTION set_updated_at_field();

INSERT INTO feed_flag_status (status) VALUES 
('active'), ('always-parse'), ('spam'), ('pending-archive'), ('archived'), ('takedown'),
('parse_error'), ('fetch_error');

--** FEED

-- The top-level table for storing feed data, and internal parsing data.
CREATE TABLE feed (
    id SERIAL PRIMARY KEY,
    url varchar_url UNIQUE NOT NULL,

    -- feed flag
    feed_flag_status_id INTEGER NOT NULL REFERENCES feed_flag_status(id),

    -- internal

    -- Used to prevent another thread from parsing the same feed.
    -- Set to current time at beginning of parsing, and NULL at end of parsing. 
    -- This is to prevent multiple threads from parsing the same feed.
    -- If is_parsing is over X minutes old, assume last parsing failed and proceed to parse.
    is_parsing BOOLEAN DEFAULT FALSE,


    -- 0 will only be parsed when PI API reports an update.
    -- higher parsing_priority will be parsed more frequently on a schedule.
    parsing_priority INTEGER DEFAULT 0 CHECK (parsing_priority BETWEEN 0 AND 5),

    -- the hash of the last parsed feed file.
    -- used for comparison to determine if full re-parsing is needed.
    last_parsed_file_hash varchar_md5,

    -- the run-time environment container id
    container_id VARCHAR(12),

    created_at server_time_with_default,
    updated_at server_time_with_default
);

CREATE INDEX idx_feed_feed_flag_status_id ON feed(feed_flag_status_id);

CREATE TRIGGER set_updated_at_feed
BEFORE UPDATE ON feed
FOR EACH ROW
EXECUTE FUNCTION set_updated_at_field();

CREATE TABLE feed_log (
    id SERIAL PRIMARY KEY,
    feed_id INTEGER NOT NULL REFERENCES feed(id) ON DELETE CASCADE,
    last_http_status INTEGER,
    last_good_http_status_time server_time,
    last_finished_parse_time server_time,
    parse_errors INTEGER DEFAULT 0,
    message varchar_normal
);

CREATE INDEX idx_feed_log_feed_id ON feed_log(feed_id);


--** CHANNEL

-- <channel>
CREATE TABLE channel (
    id SERIAL PRIMARY KEY,
    id_text short_id_v2 UNIQUE NOT NULL,
    slug varchar_slug,
    feed_id INTEGER NOT NULL REFERENCES feed(id) ON DELETE CASCADE,
    podcast_index_id INTEGER UNIQUE NOT NULL,
    podcast_guid UUID UNIQUE, -- <podcast:guid>
    title varchar_normal,
    sortable_title varchar_short, -- all lowercase, ignores articles at beginning of title
    medium_id INTEGER REFERENCES medium(id),

    -- channels that have a PI value tag require special handling to request value data
    -- from the Podcast Index API.
    has_podcast_index_value BOOLEAN DEFAULT FALSE,

    -- this column is used for optimization purposes to determine if all of the items
    -- for a channel need to have their value time split remote items parsed.
    has_value_time_splits BOOLEAN DEFAULT FALSE
);

CREATE UNIQUE INDEX channel_podcast_guid_unique ON channel(podcast_guid) WHERE podcast_guid IS NOT NULL;
CREATE UNIQUE INDEX channel_slug ON channel(slug) WHERE slug IS NOT NULL;
CREATE INDEX idx_channel_feed_id ON channel(feed_id);
CREATE INDEX idx_channel_medium_id ON channel(medium_id);

--** CHANNEL > CATEGORY

-- <channel> -> <category>
CREATE TABLE channel_category (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER NOT NULL REFERENCES channel(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES category(id) ON DELETE CASCADE
);

CREATE INDEX idx_channel_category_channel_id ON channel_category(channel_id);
CREATE INDEX idx_channel_category_category_id ON channel_category(category_id);


--** ITEM > FLAG STATUS

-- used internally for identifying and handling special flag statuses for items.
CREATE TABLE item_flag_status (
    id SERIAL PRIMARY KEY,
    status TEXT UNIQUE CHECK (status IN ('active', 'pending-archive', 'archived', 'pending-delete')),
    created_at server_time_with_default,
    updated_at server_time_with_default
);

CREATE TRIGGER set_updated_at_item_flag_status
BEFORE UPDATE ON item_flag_status
FOR EACH ROW
EXECUTE FUNCTION set_updated_at_field();

INSERT INTO item_flag_status (status) VALUES ('active'), ('pending-archive'), ('archived'), ('pending-delete');

--** ITEM

-- Technically the item table could be named channel_item, but it seems easier to understand as item.

-- <channel> -> <item>
CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    id_text short_id_v2 UNIQUE NOT NULL,
    slug varchar_slug,
    channel_id INTEGER NOT NULL REFERENCES channel(id) ON DELETE CASCADE,
    guid varchar_uri, -- <guid>
    guid_enclosure_url varchar_url, -- enclosure url
    pub_date TIMESTAMPTZ, -- <pubDate>
    title varchar_normal, -- <title>

    item_flag_status_id INTEGER NOT NULL REFERENCES item_flag_status(id),
    
    -- Ensure either guid or guid_enclosure_url is required
    CHECK (guid IS NOT NULL OR guid_enclosure_url IS NOT NULL)
);

CREATE UNIQUE INDEX item_slug ON item(slug) WHERE slug IS NOT NULL;
CREATE INDEX idx_item_channel_id ON item(channel_id);
CREATE INDEX idx_item_guid ON item(guid);
CREATE INDEX idx_item_guid_enclosure_url ON item(guid_enclosure_url);
CREATE INDEX idx_item_item_flag_status_id ON item(item_flag_status_id);


CREATE TABLE sharable_status (
    id SERIAL PRIMARY KEY,
    status TEXT UNIQUE CHECK (status IN ('public', 'unlisted', 'private'))
);

INSERT INTO sharable_status (status) VALUES ('public'), ('unlisted'), ('private');

CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    id_text short_id_v2 UNIQUE NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    sharable_status_id INTEGER NOT NULL REFERENCES sharable_status(id)
);

CREATE INDEX idx_account_sharable_status_id ON account(sharable_status_id);

-- STATS_TRACK_ACCOUNT_GUID --
CREATE TABLE stats_track_account_guid (
    id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    account_guid UUID NOT NULL,
    updated_at server_time_with_default NOT NULL,
    UNIQUE (account_id),
    UNIQUE (account_guid),
    FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE
);

CREATE INDEX stats_track_account_guid_account_id_idx ON stats_track_account_guid(account_id);
CREATE INDEX stats_track_account_guid_account_guid_idx ON stats_track_account_guid(account_guid);
CREATE INDEX stats_track_account_guid_updated_at_idx ON stats_track_account_guid(updated_at);

CREATE TABLE stats_track_event_channel (
    id SERIAL PRIMARY KEY,
    account_guid UUID NOT NULL,
    channel_id INT NOT NULL,
    created_at server_time_with_default NOT NULL,
    UNIQUE (account_guid, channel_id),
    FOREIGN KEY (account_guid) REFERENCES stats_track_account_guid(account_guid) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channel(id) ON DELETE CASCADE
);

CREATE INDEX stats_track_event_channel_account_guid_idx ON stats_track_event_channel(account_guid);
CREATE INDEX stats_track_event_channel_channel_id_idx ON stats_track_event_channel(channel_id);
CREATE INDEX stats_track_event_channel_created_at_idx ON stats_track_event_channel(created_at);

CREATE TABLE stats_aggregated_channel (
    id SERIAL PRIMARY KEY,
    channel_id INT NOT NULL,
    day_current_count INT NOT NULL DEFAULT 0,
    day_1_count INT NOT NULL DEFAULT 0,
    day_2_count INT NOT NULL DEFAULT 0,
    day_3_count INT NOT NULL DEFAULT 0,
    day_4_count INT NOT NULL DEFAULT 0,
    day_5_count INT NOT NULL DEFAULT 0,
    day_6_count INT NOT NULL DEFAULT 0,
    day_7_count INT NOT NULL DEFAULT 0,
    day_8_count INT NOT NULL DEFAULT 0,
    week_current_count INT NOT NULL DEFAULT 0,
    week_1_count INT NOT NULL DEFAULT 0,
    week_2_count INT NOT NULL DEFAULT 0,
    week_3_count INT NOT NULL DEFAULT 0,
    week_4_count INT NOT NULL DEFAULT 0,
    month_current_count INT NOT NULL DEFAULT 0,
    month_1_count INT NOT NULL DEFAULT 0,
    all_time_count INT NOT NULL DEFAULT 0,
    UNIQUE (channel_id),
    FOREIGN KEY (channel_id) REFERENCES channel(id) ON DELETE CASCADE
);

CREATE INDEX stats_aggregated_channel_channel_id_idx ON stats_aggregated_channel(channel_id);
CREATE INDEX stats_aggregated_channel_day_current_count_idx ON stats_aggregated_channel(day_current_count);
CREATE INDEX stats_aggregated_channel_week_current_count_idx ON stats_aggregated_channel(week_current_count);
CREATE INDEX stats_aggregated_channel_month_current_count_idx ON stats_aggregated_channel(month_current_count);
CREATE INDEX stats_aggregated_channel_all_time_count_idx ON stats_aggregated_channel(all_time_count);

CREATE TABLE stats_track_event_item (
    id SERIAL PRIMARY KEY,
    account_guid UUID NOT NULL,
    item_id INT NOT NULL,
    created_at server_time_with_default NOT NULL,
    UNIQUE (account_guid, item_id),
    FOREIGN KEY (account_guid) REFERENCES stats_track_account_guid(account_guid) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE
);

CREATE INDEX stats_track_event_item_account_guid_idx ON stats_track_event_item(account_guid);
CREATE INDEX stats_track_event_item_item_id_idx ON stats_track_event_item(item_id);
CREATE INDEX stats_track_event_item_created_at_idx ON stats_track_event_item(created_at);

CREATE TABLE stats_aggregated_item (
    id SERIAL PRIMARY KEY,
    item_id INT NOT NULL,
    day_current_count INT NOT NULL DEFAULT 0,
    day_1_count INT NOT NULL DEFAULT 0,
    day_2_count INT NOT NULL DEFAULT 0,
    day_3_count INT NOT NULL DEFAULT 0,
    day_4_count INT NOT NULL DEFAULT 0,
    day_5_count INT NOT NULL DEFAULT 0,
    day_6_count INT NOT NULL DEFAULT 0,
    day_7_count INT NOT NULL DEFAULT 0,
    day_8_count INT NOT NULL DEFAULT 0,
    week_current_count INT NOT NULL DEFAULT 0,
    week_1_count INT NOT NULL DEFAULT 0,
    week_2_count INT NOT NULL DEFAULT 0,
    week_3_count INT NOT NULL DEFAULT 0,
    week_4_count INT NOT NULL DEFAULT 0,
    month_current_count INT NOT NULL DEFAULT 0,
    month_1_count INT NOT NULL DEFAULT 0,
    all_time_count INT NOT NULL DEFAULT 0,
    UNIQUE (item_id),
    FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE
);

CREATE INDEX stats_aggregated_item_item_id_idx ON stats_aggregated_item(item_id);
CREATE INDEX stats_aggregated_item_day_current_count_idx ON stats_aggregated_item(day_current_count);
CREATE INDEX stats_aggregated_item_week_current_count_idx ON stats_aggregated_item(week_current_count);
CREATE INDEX stats_aggregated_item_month_current_count_idx ON stats_aggregated_item(month_current_count);
CREATE INDEX stats_aggregated_item_all_time_count_idx ON stats_aggregated_item(all_time_count);
