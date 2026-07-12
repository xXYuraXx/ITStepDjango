#!/usr/bin/env bash

echo "=== Running Database Migrations ==="
python manage.py migrate --noinput || echo "Migrations skipped."

echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput || echo "Static files collection skipped."

echo "=== Loading Fixtures ==="
python manage.py loaddata tests.json || echo "Fixtures skipped."


echo "=== Starting Application ==="
exec "$@"