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
from datetime import datetime

sys.path.insert(0, 'vaderSentiment/vaderSentiment')
from vaderSentiment import SentimentIntensityAnalyzer

import globalLists as gl
import medium as m
import sentiment


# TIME_PERIOD = 60 * 60 * 1000# How far you want to go back in the subreddit
# SUBREDDIT = 'wallstreetbets'

a = time.time()

# Large comment threads
large_threads=[]

def crawl_subreddit(subreddit):
    try:
        # Create praw connection
        reddit = praw.Reddit(client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRETS,
                            user_agent='Comment extraction by /u/PartialSyntax')
        # iterate through latest 24 hours of submissions and all comments made on those submissions
        timestamp = int(time.time())
        for submission in reddit.subreddit(SUBREDDIT).new(limit=1000):
            time_delta = timestamp - submission.created_utc
            m.addPost(submission)
            if (time_delta > TIME_PERIOD):
                break
            # seen = dbm.checkPost(submission.id)
            # if (submission.num_comments<1000):
            #     print(submission.num_comments)
            #     sentiment.analyze_text(submission)
            # count = dbm.getCommentCount(submission)
            # if(seen and count == submission.num_comments):
            #     continue
                            
            # Parses post comments
            try:
                for comment in submission.comments.list():
                    if(type(comment)==praw.models.reddit.more.MoreComments):
                        continue
                    if (submission.num_comments > 999):
                        large_threads.append(submission.id)
                        print(submission.id)
                        break
                    else:
                        sentiment.analyze_text(comment)

            except Exception as e:
                print(e)
            last_time = submission.created_utc
        return last_time
    except:
        pass


def main():
    # pickup = crawl_subreddit("wallstreetbets")
    pickup = time.time()
    # crawl_subreddit(SUBREDDIT)
    m.getHistory(pickup)
    # m.largeLoop(large_threads)


if __name__ == "__main__":
    TIME_PERIOD = 60 * 60 * 60# How far you want to go back in the subreddit
    SUBREDDIT = 'wallstreetbets'
    a = time.time()
    main()
    print(time.time()-a)