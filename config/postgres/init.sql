-- DROP TABLE IF EXISTS submissions;

CREATE TABLE IF NOT EXISTS submissions (
    id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    selftext TEXT,
    score INTEGER,
    num_comments INTEGER,
    created_utc TIMESTAMP,
    vector JSONB
);
