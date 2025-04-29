from app.celery_app import app
from app.utils import RedditScraper, get_submission_info
import requests
from time import perf_counter



@app.task
def reddit_submissions(subreddit_name: str, 
                       limit: int) -> None:
    """
    Fetch Reddit submissions and update Prometheus metrics.

    Args:
        subreddit_name (str): The name of the subreddit.
        limit (int): The maximum number of submissions to retrieve.
    
    Returns:
        None
    """
    reddit = RedditScraper()

    start = perf_counter()
    submissions = reddit.get_submissions(subreddit_name, limit)
    end = perf_counter()
    duration = end - start
    print(f'Ilość wpisów: {len(submissions)}')

    try:
        requests.post(f"http://metrics_server:8000/observe_time/{duration}")
    except Exception as e:
        print(f"Failed to send duration metric: {e}")
    
    try:
        requests.post(f"http://metrics_server:8000/set_post_count/{len(submissions)}")
    except Exception as e:
        print(f"Failed to send post count: {e}")


    for s in submissions:
        submission_data = get_submission_info(s)
        score = submission_data['score']
        comments = submission_data['num_comments']

        try:
            requests.post("http://metrics_server:8000/update_metrics/", params={
                "score": score,
                "comments": comments
            })
        except Exception as e:
            print(f"Failed to send post metrics: {e}")

        print(f"Score: {score}, komentarze: {comments}")
