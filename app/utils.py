from dotenv import load_dotenv
import os
import praw



class RedditScraper:
    """
    A class to scrape Reddit submissions using the PRAW library.
    """

    def __init__(self):
        """
        Initialize the RedditScraper class and authenticate with Reddit API.
        """
        self.reddit = self.__reddit_auth()
    

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
        reddit = praw.Reddit(**reddit_credentials)
        return reddit


    def get_submissions(self, 
                        subreddit_name: str,
                        limit: int) -> tuple:
        """
        Return a list of Reddit submissions and their IDs.

        Args:
            subreddit_name (str): The name of the subreddit.
            limit (int): The maximum number of submissions to retrieve.
        
        Returns:
            tuple: A tuple containing a list of submissions and a list of their IDs.
        """

        subreddit = self.reddit.subreddit(subreddit_name)
        submissions = list(subreddit.new(limit=limit))
        return submissions





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