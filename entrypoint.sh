#!/bin/bash

# Wait for the PostgreSQL database to be ready
/usr/local/bin/wait-for db:5432 --timeout=30

# Apply migrations
python manage.py migrate

# Load database fixtures
python manage.py loaddata fixtures/users.json fixtures/books.json

# Start the Django development server
python manage.py runserver 0.0.0.0:8080
