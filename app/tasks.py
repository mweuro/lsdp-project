from app.celery_app import app
from app.utils.database import is_data_new
from app.utils.language_detection import get_model, is_polish
from app.utils.reddit import RedditScraper, get_submission_info
from app.utils.vectorizer import get_model as get_vectorizer_model
from celery import chain, chord, group
from celery.exceptions import Ignore
import datetime
from dotenv import load_dotenv
from itertools import islice
import json
import os
import psycopg2
from psycopg2.extras import execute_values
import re
import requests
from time import perf_counter


load_dotenv("postgres.env")
POSTGRES_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT"))
}


@app.task
def reddit_scraper(subreddit: str, limit: int) -> list:
    reddit = RedditScraper()
    submissions = reddit.get_submissions(subreddit, limit)
    keys = [
        "id",
        "title",
        "author",
        "selftext",
        "score",
        "num_comments",
        "created_utc",
    ]

    all_filtered = []
    for submission in submissions:
        submission_data = get_submission_info(submission)
        filtered_data = {key: submission_data[key] for key in keys if key in submission_data}
        all_filtered.append(filtered_data)

    return all_filtered


@app.task
def language_detection(submissions: list) -> list:
    old_submissions, new_submissions = is_data_new(submissions)
    updated_submissions = []

    if not new_submissions:
        updated_submissions.extend(old_submissions)
    else:
        detector = get_model()
        for submission_data in old_submissions:
            updated_submissions.append(submission_data)
        for submission_data in new_submissions:
            title = submission_data.get("title", "")
            title = " ".join(title.replace("\n", " ").strip().split())
            title = re.sub(r"http\S+|www\S+|https\S+", " ", title, flags=re.MULTILINE)
            try:
                label = detector.detect_language(title)
                if is_polish(label):
                    updated_submissions.append(submission_data)
            except ValueError:
                pass

    return updated_submissions


@app.task
def vectorization(submissions: list) -> list:
    old_submissions, new_submissions = is_data_new(submissions)
    updated_submissions = []
    vectorizer = get_vectorizer_model()

    for submission_data in old_submissions:
        title = submission_data.get("title", "")
        selftext = submission_data.get("selftext", "")
        text_to_vectorize = selftext if selftext else title
        embeddings = vectorizer.vectorize(text_to_vectorize)
        submission_data["vector"] = [float(x) for x in embeddings]
        updated_submissions.append(submission_data)

    for submission_data in new_submissions:
        title = submission_data.get("title", "")
        selftext = submission_data.get("selftext", "")
        text_to_vectorize = selftext if selftext else title
        embeddings = vectorizer.vectorize(text_to_vectorize)
        submission_data["vector"] = [float(x) for x in embeddings]
        updated_submissions.append(submission_data)

    return updated_submissions


@app.task
def save_to_postgresql(submissions: list) -> None:
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cur = conn.cursor()

        rows = []
        for sub in submissions:
            created_ts = sub.get("created_utc")
            created_utc = (
                datetime.datetime.fromtimestamp(created_ts)
                if created_ts is not None else None
            )
            rows.append((
                sub.get("id"),
                sub.get("title"),
                sub.get("author"),
                sub.get("selftext"),
                sub.get("score"),
                sub.get("num_comments"),
                created_utc,
                json.dumps(sub.get("vector")) if "vector" in sub else None
            ))

        query = """
            INSERT INTO submissions (id, title, author, selftext, score, num_comments, created_utc, vector)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                author = EXCLUDED.author,
                selftext = EXCLUDED.selftext,
                score = EXCLUDED.score,
                num_comments = EXCLUDED.num_comments,
                created_utc = EXCLUDED.created_utc,
                vector = EXCLUDED.vector;
        """

        execute_values(cur, query, rows)
        conn.commit()
    except Exception as e:
        pass
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


@app.task
def pipeline(subreddit: str, limit: int):
    task_chain = chain(
        reddit_scraper.s(subreddit, limit),
        language_detection.s(),
        vectorization.s(),
        save_to_postgresql.s()
    )
    task_chain.apply_async()