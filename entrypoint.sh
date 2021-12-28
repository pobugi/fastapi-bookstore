#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z py-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Run migrations"
/venv/bin/alembic upgrade head

echo "Run service"
exec "$@"
