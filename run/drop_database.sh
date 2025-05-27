#!/bin/bash

docker exec -it postgres psql -U reddit -d postgres -c "DROP DATABASE IF EXISTS reddit_data;"
echo "Database 'reddit_data' dropped (if it existed)."