#!/bin/sh

until pg_isready -h postgres -U "$POSTGRES_USER"; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

python -m api.db
