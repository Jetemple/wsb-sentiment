import config
import json
import csv
import praw
from praw.models import MoreComments
import time
import os
import logging
import sys
import yfinance as yf
import requests
from string import punctuation
import sqlConnect as dbm
from datetime import datetime

sys.path.insert(0, 'vaderSentiment/vaderSentiment')
from vaderSentiment import SentimentIntensityAnalyzer

import globalLists as gl
import pushshift as ps
import sentiment


# TIME_PERIOD = 60 * 60 * 1000# How far you want to go back in the subreddit
# SUBREDDIT = 'wallstreetbets'

a = time.time()

# Large comment threads
large_threads=[]

ticker_dict = {} # Holds all of the tickers

def crawl_subreddit(subreddit):
    # Create praw connection
    reddit = praw.Reddit(client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRETS,
                         user_agent='Comment extraction by /u/PartialSyntax')
    # iterate through latest 24 hours of submissions and all comments made on those submissions
    timestamp = int(time.time())
    for submission in reddit.subreddit(SUBREDDIT).new(limit=1000):
        time_delta = timestamp - submission.created_utc
        if (time_delta > TIME_PERIOD):
            break
        seen = dbm.checkPost(submission.id)
        if not (seen and submission.num_comments<1000):
            dbm.addPost(submission.id, submission.num_comments, submission.created_utc)
    
            sentiment.analyze_text(submission)
        count = dbm.getCommentCount(submission)
        if(seen and count == submission.num_comments):
            continue
                        
        # Parses post comments
        try:
            for comment in submission.comments.list():
                # if(type(comment)==praw.models.reddit.more.MoreComments):
                #     continue
                if (submission.num_comments > 999):
                    large_threads.append(submission.id)
                    print(submission.id)
                    break
                if not(dbm.checkComment(comment.id)):
                    # continue
                    sentiment.analyze_text(comment)

        except Exception as e:
            print(e)
        last_time = submission.created_utc
    return last_time


def main():
    # pickup = crawl_subreddit("wallstreetbets")
    pickup = time.time()
    ps.getHistory(pickup)
    ps.largeLoop(large_threads)


if __name__ == "__main__":
    TIME_PERIOD = 60 * 60 * 1000 # How far you want to go back in the subreddit
    SUBREDDIT = 'wallstreetbets'
    a = time.time()
    main()
    print(time.time()-a)