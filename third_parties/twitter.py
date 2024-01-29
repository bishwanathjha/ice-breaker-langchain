import os
from datetime import datetime, timezone
import logging
from dotenv import load_dotenv

import tweepy

load_dotenv()

logger = logging.getLogger("tweepy")

auth = tweepy.OAuthHandler(
    os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET")
)
auth.set_access_token(
    os.environ.get("TWITTER_ACCESS_TOKEN"), os.environ.get("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)


def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    if os.environ.get("TWITTER_SAMPLE") == "1":
        return _get_sample_data()

    tweets = api.user_timeline(screen_name=username, count=num_tweets)

    return _clean_response(tweets)


def _get_sample_data():
    posts = [
        {
            "time_posted": "2 days ago",
            "text": "LangGraph beats AutoGen: How Future of Internet Search will look like? for highlighting LangGraph in his most recent YouTube video!",
            "url": "https://twitter.com/BishwanathJha/status/1600620085437145110",
        },
        {
            "time_posted": "5 days ago",
            "text": "Build LLM Data Apps with LangChain and Dash Join us next week for a joint webinar featuring community-built Dash apps These apps won the Dash/LangChain build challenge - so you know they re the best of the best",
            "url": "https://twitter.com/BishwanathJha/status/1600620085437145112",
        },
    ]
    return posts


def _clean_response(response: dict) -> list:
    tweet_list = []

    for tweet in response:
        # We are doing some cleanup here as we do not need re-tweet as to start with RT or starts with @ sign
        if "RT @" not in tweet.text and not tweet.text.startswith("@"):
            tweet_dict = {
                "time_posted": str(datetime.now(timezone.utc) - tweet.created_at),
                "text": tweet.text,
                "url": f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",
            }
            tweet_list.append(tweet_dict)

    return tweet_list
