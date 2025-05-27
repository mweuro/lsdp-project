from psycopg2 import connect
from psycopg2.extras import execute_values
import numpy as np


POSTGRES_CONFIG = {
    "dbname": "reddit_data",
    "user": "reddit",
    "password": "reddit",
    "host": "postgres",
    "port": 5432
}



def is_data_new(submissions: list) -> tuple[list, list]:
    # Jeśli zgłoszenia są zagnieżdżone (np. [[{...}, {...}, ...]]), spłaszcz je.
    if submissions and isinstance(submissions[0], list):
        submissions = submissions[0]
        
    print(f"Submissions data: {submissions}")
    conn = connect(**POSTGRES_CONFIG)
    cur = conn.cursor()

    all_ids = [s["id"] for s in submissions]
    cur.execute("SELECT id FROM submissions WHERE id = ANY(%s);", (all_ids,))
    existing_ids = {row[0] for row in cur.fetchall()}

    old_submissions = []
    new_submissions = []
    for submission in submissions:
        if submission["id"] in existing_ids:
            old_submissions.append(submission)
        else:
            new_submissions.append(submission)

    cur.close()
    conn.close()

    return old_submissions, new_submissions

