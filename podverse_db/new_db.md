# Podverse Database Schema Overview

This document explains the new simplified database schema designed to consolidate Podverse's data structure. The goal is to reduce complexity by consolidating related data into fewer tables, leveraging PostgreSQL's JSONB support for flexible metadata storage.

---

## Schema Summary

| Table Name     | Purpose                                      | Key Relationships                            |
|----------------|----------------------------------------------|---------------------------------------------|
| **account**    | User accounts with profile, settings, memberships | Primary key `id`                             |
| **podcast**    | Podcast channels with metadata                | Primary key `id`                             |
| **episode**    | Podcast episodes linked to podcasts           | Foreign key `podcast_id` references podcast |
| **feed**       | Raw podcast feed URLs & fetch status          | Primary key `id`                             |
| **playlist**   | User-created playlists with episode order     | Foreign key `account_id` references account |
| **subscription** | Tracks follows/subscriptions (podcasts, accounts, etc.) | Foreign key `account_id` references account |
| **stats**      | Aggregated listening stats for any entity     | Tracks entity by type and ID                 |
| **media**      | Clips, soundbites, and media assets linked to episodes | Foreign key `episode_id` references episode |
| **notifications** | User notification preferences                 | Foreign key `account_id` references account |

---

## Table Details

### 1. `account`

- Stores user credentials plus additional flexible profile and settings data.
- `profile`, `settings`, and `memberships` are stored as JSONB columns for easy extensibility.
- Enables personalized experiences without schema changes for new profile features.

### 2. `podcast`

- Main table for podcast channels.
- Categories and metadata stored as JSONB arrays/objects.
- Keeps podcast info compact and extensible.

### 3. `episode`

- Linked to `podcast` by `podcast_id`.
- Stores episode-level metadata like media URLs, transcripts, and statistics in JSONB.
- Allows flexible expansion without table sprawl.

### 4. `feed`

- Maintains raw feed URLs and fetch status metadata.
- Useful for backend ingestion and feed management.

### 5. `playlist`

- User playlists, storing ordered episode IDs as an integer array.
- `metadata` JSONB for playlist descriptions, privacy settings, etc.
- Supports flexible playlist features without additional tables.

### 6. `subscription`

- Tracks what accounts are following (podcasts, other accounts, etc.).
- `target_type` allows a generic follow system adaptable to future entity types.
- Unique constraint prevents duplicate subscriptions.

### 7. `stats`

- Centralizes all entity stats (podcasts, episodes, accounts) in a single table.
- Indexed by `entity_type` and `entity_id` to support efficient lookups.
- Supports daily stats aggregation.

### 8. `media`

- Stores media clips, soundbites, and additional episode media assets.
- Metadata stored in JSONB (e.g., encoding info, thumbnails).
- Linked directly to episodes.

### 9. `notifications`

- User notification preferences stored as JSONB.
- Designed for flexible preference options without schema changes.

---

## Why JSONB?

- Flexible storage format for semi-structured data.
- Allows adding new fields without database migrations.
- Efficient querying and indexing capabilities in PostgreSQL.

---

## Indexing & Performance

- Key indexes on foreign keys and JSONB fields ensure efficient query performance.
- Example: `GIN` index on `podcast.categories` JSONB array enables fast category filtering.
- `stats` table indexed for quick aggregation queries.

---

## Extensibility

- This schema is designed to evolve gracefully.
- Adding new metadata or entity types typically means extending JSONB columns or adding entries in `target_type` enums.
- Reduces overhead of schema migrations and keeps the database manageable.

---

## Migration & Integration

- Existing data can be merged or transformed into this schema using ETL or migration scripts.
- APIs and backend logic should be updated to use JSONB fields and the consolidated tables.
- Client-side code can remain mostly unchanged, with backend handling data flattening.

---

## Summary

This consolidated schema reduces complexity while maintaining flexibility and scalability:

- From 97+ tables down to ~9 core tables
- Rich metadata support with JSONB
- Flexible follow system with subscriptions
- Centralized stats tracking per entity
- Playlist and notification management simplified

