import config
import json
import csv
import praw
from praw.models import MoreComments
import time
import os
import logging
import sys
import requests
from string import punctuation
from datetime import datetime

import globalLists as gl

sys.path.insert(0, 'vaderSentiment/vaderSentiment')
from vaderSentiment import SentimentIntensityAnalyzer


BASE_URL = config.BASE_URL

def findTicker(body):
    # Finds the ticker in the title
    for word in body.split():
        word = word.strip(punctuation)
        word = word.upper()
        if gl.ALTERNATE_SPELLING.get(word) != None:
            word = gl.ALTERNATE_SPELLING.get(word)
        if (len(word) < 2):
            continue
        # Does word fit the ticker criteria
        if len(word) != 1 and (word not in gl.COMMON_WORDS) and len(word) <= 5 and word.isalpha() and (word.upper() in gl.TICKERS):
            return word


def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    if (sentiment["compound"] > .005) or (sentiment["pos"] > abs(sentiment["neg"])):
        return "Bullish"
    elif (sentiment["compound"] < -.005) or (abs(sentiment["neg"]) > sentiment["pos"]):
        return "Bearish"
    else:
        return "Neutral"
