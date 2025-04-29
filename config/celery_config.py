from dotenv import load_dotenv
import os
from celery.schedules import schedule

# Load reddit.env
load_dotenv("reddit.env")

# Serialization settings
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

# Celery config
broker_url = "amqp://user:password@rabbitmq:5672/"
result_backend = "rpc://"

# Timezone settings
timezone = 'Europe/Warsaw'
enable_utc = True

# Params from environment
SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME", "AskReddit")
SUBMISSION_LIMIT = int(os.getenv("SUBMISSION_LIMIT", 10))
SCHEDULE_TIME = float(os.getenv("SCHEDULE_TIME", 20.0))

# Celery beat schedule
beat_schedule = {
    'reddit_submissions': {
        'task': 'app.tasks.reddit_submissions',
        'schedule': schedule(SCHEDULE_TIME),
        'kwargs': {
            'subreddit_name': SUBREDDIT_NAME,
            'limit': SUBMISSION_LIMIT
        }
    }
}