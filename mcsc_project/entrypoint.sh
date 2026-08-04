#!/bin/sh
set -e

echo "=== MCSC Portal Docker Entrypoint ==="

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --no-input

echo "Startup complete. Launching application server..."
exec "$@"
