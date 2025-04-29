from prometheus_client import Counter, Gauge, Summary, Histogram


SCORE_HISTOGRAM = Histogram('reddit_post_score', 'Histogram of Reddit post scores', buckets=(0, 10, 50, 100, 500, 1000, 5000))
COMMENT_HISTOGRAM = Histogram('reddit_post_comments', 'Histogram of Reddit post comments', buckets=(0, 10, 50, 100, 500, 1000))
FETCH_TIME_SUMMARY = Summary('reddit_fetch_duration_seconds', 'Time spent fetching Reddit posts')
POST_COUNT_GAUGE = Gauge('reddit_fetched_posts', 'Number of Reddit posts fetched')
POSTS_FETCHED_COUNTER = Counter('reddit_posts_fetched_total', 'Total number of Reddit posts fetched')
