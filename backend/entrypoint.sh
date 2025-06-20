#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

until pg_isready -h database -p 5432 -U podverse_admin > /dev/null 2>&1; do
  echo "Postgres is unavailable - sleeping for 2 seconds"
  sleep 2
done

echo "PostgreSQL is up - continuing..."

echo "Running dummy data generation script..."
python ./scripts/generate_dummy_users.py || echo "Dummy data script failed or already run, continuing..."

echo "Starting Flask app..."
exec python main.py