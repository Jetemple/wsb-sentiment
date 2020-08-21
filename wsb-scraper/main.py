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
from string import punctuation
import dbm

sys.path.insert(0, 'vaderSentiment/vaderSentiment')
from vaderSentiment import SentimentIntensityAnalyzer


TIME_PERIOD = 60 * 60 * 9# How far you want to go back in the subreddit
SUBREDDIT = 'wallstreetbets'

a = time.time()
class Ticker:
    def __init__(self, ticker):
        self.ticker = ticker
        self.count = 0
        self.bodies = []
        self.pos_count = 0
        self.neg_count = 0
        self.bullish = 0
        self.bearish = 0
        self.neutral = 0
        self.sentiment = 0  # 0 is neutral

    def analyze_sentiment(self):
        analyzer = SentimentIntensityAnalyzer()
        neutral_count = 0
        for text in self.bodies:
            sentiment = analyzer.polarity_scores(text)
            if (sentiment["compound"] > .005) or (sentiment["pos"] > abs(sentiment["neg"])):
                self.pos_count += 1
            elif (sentiment["compound"] < -.005) or (abs(sentiment["neg"]) > sentiment["pos"]):
                self.neg_count += 1
            else:
                neutral_count += 1
        self.bullish = int(self.pos_count / len(self.bodies) * 100)
        self.bearish = int(self.neg_count / len(self.bodies) * 100)
        self.neutral = int(neutral_count / len(self.bodies) * 100)



def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    if (sentiment["compound"] > .005) or (sentiment["pos"] > abs(sentiment["neg"])):
        return "Bullish"
    elif (sentiment["compound"] < -.005) or (abs(sentiment["neg"]) > sentiment["pos"]):
        return "Bearish"
    else:
        return "Neutral"

# Large comment threads
large_threads=[]

# list of common english words to remove
common_word_filters = ["SON","USD","IPO","PDT","ATH","ITM","YOLO","EPS","AUG", "CEO", "GOLD", "ALOT", "JAN", "ONCE", "EDIT", "BRO", "SU", "LIFE", "CFO", "JOB", "BIT", "TWO", "BEST", "BIG", "EOD", "HOPE", "AM", "EVER", "PUMP", "NEXT", "HE", "REAL", "WORK", "NICE", "TOO", "MAN", "LOVE", "BY", "VERY", "ANY", "SEE",
                       "NEW", "WELL", "TELL", "IT", "ONE", "POST", "ON", "TURN", "GOOD", "CAN", "HAS", "GO", "PLAY", "ELSE", "GAIN", "RUN", "INFO", "STAY", "CARE", "ALL", "AT", "PER", "DO", "ARE", "NOW", "BE", "OR", "SO", "OUT", "BEAT", "AGO", "AN", "PEAK", "LOW", "DD", "FOR", "FLAT"]

ticker_dict = {} # Holds all of the tickers
tickers = open("symbols.txt").read().splitlines()# Holds all of the tickers

# Checks to see if there are tickers in the word
def analyze_text(item):
    post = type(item) == praw.models.reddit.submission.Submission
    if(post):
        text = item.title
        text = text + (item.selftext)
    else:
        text = item.body
    time = item.created_utc
    id = item.id
    
    for word in text.split():
        word = word.rstrip(punctuation)

        if (len(word) < 3):
            continue
 
        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in common_word_filters) and len(word) <= 5 and word.isalpha() and (word.upper() in tickers):
            # Checks to see if the ticker has been cached.
            sentiment = analyze_sentiment(text)
            if (word in ticker_dict):
                ticker_dict[word].count += 1
                ticker_dict[word].bodies.append(text)
            else:
                ticker_dict[word] = Ticker(word)
                ticker_dict[word].count = 1
                ticker_dict[word].bodies.append(text)
            dbm.addTicker(word)
            if not(post):
                dbm.addComment(id,time,word, item.link_id, text, sentiment)
    return ticker_dict


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
        if not (seen):
            dbm.addPost(submission.id, submission.num_comments, submission.created_utc)
            ticker_dict = analyze_text(submission)
            old = False
        count = dbm.getCommentCount(submission)
        if(seen and count == submission.num_comments):
            continue
                        
        # Parses post comments
        for comment in submission.comments.list():
            if isinstance(comment, MoreComments):
                large_threads.append(submission.id)
                continue
            if not(dbm.checkComment(comment.id)):
                ticker_dict = analyze_text(comment)
                


crawl_subreddit("wallstreetbets")
count = {}
# for ticker in ticker_dict:
#     ticker_dict[ticker].analyze_sentiment()
#     count[ticker] = ticker_dict[ticker].count
for thread in large_threads:
    print(thread)

print("Stock \t Count \t Bullish \t Neutral \t Bearish")
for key, value in sorted(count.items(), key=lambda x: x[1], reverse=True):
    print(key, "\t", value , "\t" ,ticker_dict[key].bullish , "\t\t", ticker_dict[key].neutral , "\t\t", ticker_dict[key].bearish)