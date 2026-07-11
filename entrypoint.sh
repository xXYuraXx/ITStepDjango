#!/bin/sh

set -e

echo "=== Running Database Migrations ==="
python manage.py migrate --noinput

echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput || true

if [ -f "tests.json" ]; then
    echo "=== Loading Fixtures ==="
    python manage.py loaddata tests.json || echo "Fixtures already loaded or skipped."
fi

echo "=== Starting Application ==="
exec "$@"