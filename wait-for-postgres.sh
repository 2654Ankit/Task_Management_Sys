#!/bin/sh

# Wait until Postgres is ready
echo "Waiting for PostgreSQL..."

until pg_isready -h db -p 5432 -U "$POSTGRES_USER" > /dev/null 2>&1; do
  sleep 1
done

echo "PostgreSQL is up!"
exec "$@"
