from dotenv import load_dotenv
import os
import praw


class RedditScraper:
    """
    A Singleton class to scrape Reddit submissions using the PRAW library.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedditScraper, cls).__new__(cls, *args, **kwargs)
            cls._instance.reddit = cls._instance.__reddit_auth()
        return cls._instance

    def __reddit_auth(self) -> praw.Reddit:
        """
        Authenticate with Reddit API using environment variables.

        Returns:
            praw.Reddit: An authenticated Reddit instance.
        """
        load_dotenv()  # Load environment variables

        reddit_credentials = {
            'client_id': os.getenv('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'user_agent': os.getenv('USER_AGENT'),
            'username': os.getenv('USERNAME')
        }
        return praw.Reddit(**reddit_credentials)

    def get_submissions(self, subreddit: str, limit: int) -> list:
        """
        Return a list of Reddit submissions.

        Args:
            subreddit (str): The name of the subreddit.
            limit (int): The maximum number of submissions to retrieve.

        Returns:
            list: A list of Reddit submissions.
        """
        subreddit = self.reddit.subreddit(subreddit)
        return list(subreddit.new(limit=limit))


def get_submission_info(submission: praw.models.Submission) -> dict:
    """
    Extract relevant information from a Reddit submission.

    Args:
        submission (praw.models.Submission): The Reddit submission object.

    Returns:
        dict: A dictionary containing the submission's information.
    """
    submission_data = {
        'id': submission.id,
        'title': submission.title,
        'author': submission.author.name if submission.author else None,
        'created_utc': submission.created_utc,
        'num_comments': submission.num_comments,
        'score': submission.score,
        'selftext': submission.selftext if submission.selftext else None
    }
    return submission_data