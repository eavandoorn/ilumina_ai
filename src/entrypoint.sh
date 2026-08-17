#!/bin/bash
set -e

# Use the environment file if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
elif [ -f .env.sandbox ]; then
    export $(grep -v '^#' .env.sandbox | grep -v '^$' | xargs)
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding sandbox data..."
# We use a conditional check to ensure it only runs when needed or if the command exists
if python -c "from django.core.management import call_command; call_command('seed_sandbox')"; then
    echo "Seeding complete."
fi

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8080
