SUBREDDIT_NAME ?= AskReddit
SUBMISSION_LIMIT ?= 10
SCHEDULE_TIME ?= 20


.PHONY: venv_setup
venv_setup:
	python3.10 -m venv .venv && \
	source .venv/bin/activate && \
	pip install --upgrade pip


.PHONY: run_scraper
run_scraper:
	@echo "   Running with:"
	@export $(shell sed 's/=.*//' reddit.env)
	@echo "   SUBREDDIT_NAME=$$(SUBREDDIT_NAME)"
	@echo "   SUBMISSION_LIMIT=$$(SUBMISSION_LIMIT)"
	@echo "   SCHEDULE_TIME=$$(SCHEDULE_TIME)"
	docker-compose down && \
	SUBREDDIT_NAME=$(SUBREDDIT_NAME) \
	SUBMISSION_LIMIT=$(SUBMISSION_LIMIT) \
	SCHEDULE_TIME=$(SCHEDULE_TIME) \
	run/run_scraper.sh


enter_postgres:
	docker exec -it postgres psql -U reddit -d reddit_data
