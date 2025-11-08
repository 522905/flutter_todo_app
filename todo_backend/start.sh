#!/bin/bash

# Start script for Todo Backend

echo "🚀 Starting Todo Backend..."

# Activate virtual environment
source venv/bin/activate

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate

# Create superuser if needed (optional)
# python manage.py createsuperuser

# Start Django development server
echo "🌐 Starting Django server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/api/docs/"
echo "👤 Admin Panel: http://localhost:8000/admin/"
echo ""
python manage.py runserver

# To run Celery worker (in separate terminal):
# celery -A config worker -l info

# To run Celery beat (in separate terminal):
# celery -A config beat -l info
