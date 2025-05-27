#!/bin/bash

chmod +x "$0"

if [ -f ./redash.env ]; then
    source ./redash.env
else
    echo "redash.env file not found. Create it with variables: REDASH_ADMIN_EMAIL, REDASH_ADMIN_PASSWORD, REDASH_ADMIN_NAME."
    exit 1
fi

if docker exec -i postgres psql -U reddit -d reddit_data -tAc "SELECT 1 FROM pg_database WHERE datname='redash'" | grep -q 1; then
    echo "Redash base already exists. Skipping creation."
else
    echo "Creating Redash database..."
    docker exec -it postgres psql -U reddit -d reddit_data -c "CREATE DATABASE redash;"
fi

echo "Migrating database..."

docker-compose -p redash -f docker-compose.redash.yaml run --rm server create_db

echo "Starting Redash services..."

docker-compose -p redash -f docker-compose.redash.yaml up

echo "Redash initialization complete. You can access it at http://localhost:5001"