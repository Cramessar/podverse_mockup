How to Connect to Your Docker PostgreSQL Database and Verify Data
1. Connect to Your Backend Docker Container

```bash
Copy
docker exec -it podverse_backend sh
apt-get update
apt-get install -y postgresql-client
psql -h database -U podverse_admin -d podverse_db
enter your postgres paswword

```

psql -h database -U podverse_admin -d podverse_db
Password for user podverse_admin: 

You will be prompted for the password. Enter the password you configured in your .env or Docker Compose file (e.g., testest). I should fix the hardcoded password soon.


If you see this prompt:

```
podverse_db=#
```
You’re connected successfully to the db inside the docker container.

2.  If you are having errors or issues building the containers try these steps to break down your current containers, clear your cache and build everything from a fresh state.

```bash
docker compose down

docker builder prune --all

docker compose up --build

```


3. Run SQL Queries to Check Your Data
You can test these now:
``` bash
Users:
SELECT COUNT(*) FROM users; → Should return ~200
Check details like roles, emails, last login, etc.

Feeds:
SELECT * FROM feed LIMIT 5; → Should show ~5 fake feed URLs.

Channels:
SELECT * FROM channel LIMIT 5; → Should be linked to feeds by feed_id.

Items:
SELECT * FROM item LIMIT 5; → Each tied to a channel.

Stats tables:
Query event and aggregate tables to see relationships and counts.
```

You can also try this script to see if your db has working data, then try those sql commands again to see if anything changed.

``` bash
docker exec -it podverse_backend python /app/test_feed_insert.py
docker exec -it podverse_backend python /app/scripts/generate_dummy_users.py
```
