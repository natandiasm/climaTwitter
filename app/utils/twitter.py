import tweepy
import os
from dotenv import load_dotenv

load_dotenv()


class Twitter:
    _shared_state = {}
    api = None

    def __new__(cls):
        inst = super().__new__(cls)
        inst.__dict__ = cls._shared_state
        return inst

    def start(self) -> None:
        # Authenticate to Twitter
        self.api = tweepy.Client(bearer_token=os.getenv("TWITTER_API_BEARER"),
                                 consumer_key=os.getenv("TWITTER_API_CONSUMER_KEY"),
                                 consumer_secret=os.getenv("TWITTER_API_CONSUMER_SECRET"),
                                 access_token=os.getenv("TWITTER_API_ACCESS_TOKEN"),
                                 access_token_secret=os.getenv("TWITTER_API_ACCESS_TOKEN_SECRET"),
                                 wait_on_rate_limit=True)

    def make_tweet(self, text: str) -> None:
        self.api.create_tweet(text=text)
