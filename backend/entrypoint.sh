#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

until pg_isready -h database -p 5432 -U podverse_admin > /dev/null 2>&1; do
  echo "$(date '+%Y-%m-%d %H:%M:%S') - Postgres is unavailable - sleeping for 2 seconds"
  sleep 2
done

echo "$(date '+%Y-%m-%d %H:%M:%S') - PostgreSQL is up - continuing..."

MAX_RETRIES=5
RETRY_DELAY=5
COUNT=0

echo "$(date '+%Y-%m-%d %H:%M:%S') - Running full seed_all.py script with retries..."

while [ $COUNT -lt $MAX_RETRIES ]; do
  if python /app/scripts/seed_all.py; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Seeding completed successfully."
    break
  else
    COUNT=$((COUNT + 1))
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Seeding script failed (attempt $COUNT/$MAX_RETRIES). Retrying in $RETRY_DELAY seconds..."
    sleep $RETRY_DELAY
  fi
done

if [ $COUNT -eq $MAX_RETRIES ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') - Seeding failed after $MAX_RETRIES attempts. Continuing without seed data."
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting Flask app..."

exec python main.py