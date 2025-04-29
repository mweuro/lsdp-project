#!/bin/bash

# Default params
SUBREDDIT_NAME=${SUBREDDIT_NAME:-AskReddit}
SUBMISSION_LIMIT=${SUBMISSION_LIMIT:-10}
SCHEDULE_TIME=${SCHEDULE_TIME:-20.0}


# Generate Prometheus config
TEMPLATE_FILE="config/prometheus.template.yml"
TARGET_FILE="config/prometheus.yml"

echo "Generating prometheus.yml with scrape_interval=${SCHEDULE_TIME}s"
sed "s/{{SCRAPE_INTERVAL}}/${SCHEDULE_TIME}/g" "$TEMPLATE_FILE" > "$TARGET_FILE"


# Export params
export SUBREDDIT_NAME
export SUBMISSION_LIMIT
export SCHEDULE_TIME

echo "  Using parameters:"
echo "  SUBREDDIT_NAME=$SUBREDDIT_NAME"
echo "  SUBMISSION_LIMIT=$SUBMISSION_LIMIT"
echo "  SCHEDULE_TIME=$SCHEDULE_TIME"

# Run the task
docker-compose up --build
