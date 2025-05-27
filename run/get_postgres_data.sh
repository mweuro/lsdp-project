#!/bin/bash

CSV_FILE=${1:-submissions.csv}

container_status=$(docker inspect -f '{{.State.Running}}' postgres 2>/dev/null)

if [ "$container_status" != "true" ]; then
    echo "Postgres container is not running. Starting it now..."
    docker start postgres
    sleep 2
fi

docker exec -u postgres postgres psql -U reddit -d reddit_data -c "\copy submissions TO '/tmp/${CSV_FILE}' DELIMITER ',' CSV HEADER;"
docker cp postgres:/tmp/${CSV_FILE} ./${CSV_FILE}

echo "Ready!: ./${CSV_FILE}"
