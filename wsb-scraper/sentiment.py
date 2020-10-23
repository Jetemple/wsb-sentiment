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

import globalLists as gl

sys.path.insert(0, 'vaderSentiment/vaderSentiment')
from vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    if (sentiment["compound"] > .005) or (sentiment["pos"] > abs(sentiment["neg"])):
        return "Bullish"
    elif (sentiment["compound"] < -.005) or (abs(sentiment["neg"]) > sentiment["pos"]):
        return "Bearish"
    else:
        return "Neutral"


def analyze_text(item):
    BASE_URL = "http://localhost:3000/comments"
    isPost = type(item) == praw.models.reddit.submission.Submission
    isDict = type(item) == dict
    # awards = ''
    if(isPost):
        text = item.title
        text = text + (item.selftext)
        time = item.created_utc
        id = item.id
        score = item.score
        parent = item.id
        # awards = item.all_awardings
    elif(isDict):
        text = item['body']
        id = item['id']
        time = item['created_utc']
        score = item['score']
        parent = item['parent_id']
        if parent.startswith("t"):
            parent = parent[3:]
    else:
        text = item.body
        time = item.created_utc
        id = item.id
        score = item.score
        parent = item.link_id[3:]
        # awards = item.all_awardings

    for word in text.split():
        word = word.strip(punctuation)
        
        # Tickers of len<2 do not exist
        if (len(word) < 2):
            continue

        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in gl.common_word_filters) and len(word) <= 5 and word.isalpha() and (word.upper() in tickers):
            # Checks to see if the ticker has been cached.
            url = "http://localhost:3000/id/" + id
            r = requests.get(url= url)
            if(r.status_code == 200):
                continue
            sentiment = analyze_sentiment(text)
            print(score)
            data = {
                "comment_id" : id,
                "comment_date" : time,
                "ticker" : word,
                "parent_post" : parent,
                "body" : text,
                "score" : score,
                "sentiment" : sentiment
                }
            r = requests.post(url = BASE_URL, data = data)