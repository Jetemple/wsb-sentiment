import config
import json
import csv
import praw
import time
import os
import logging
import sys
import yfinance as yf
from string import punctuation
import sys
from tqdm import tqdm # Progress bar
import _pickle as pickle

import util

sys.path.insert(0, 'vaderSentiment/vaderSentiment')
from vaderSentiment import SentimentIntensityAnalyzer

TIME_PERIOD = 60 * 60
SUBREDDIT = 'wallstreetbets'

# Should probably get rid of these global variables
ticker_dict = {} # Holds all of the tickers
ticker_count = {}

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


# list of common english words to remove
common_word_filters = ["AUG", "CEO", "GOLD", "ALOT", "JAN", "ONCE", "EDIT", "BRO", "SU", "LIFE", "CFO", "JOB", "BIT", "TWO", "BEST", "BIG", "EOD", "HOPE", "AM", "EVER", "PUMP", "NEXT", "HE", "REAL", "WORK", "NICE", "TOO", "MAN", "LOVE", "BY", "VERY", "ANY", "SEE",
                       "NEW", "WELL", "TELL", "IT", "ONE", "POST", "ON", "TURN", "GOOD", "CAN", "HAS", "GO", "PLAY", "ELSE", "GAIN", "RUN", "INFO", "STAY", "CARE", "ALL", "AT", "PER", "DO", "ARE", "NOW", "BE", "OR", "SO", "OUT", "BEAT", "AGO", "AN", "PEAK", "LOW", "DD", "FOR", "FLAT"]


# Checks to see if there are tickers in the word
def analyze_text(text):
    for word in text.split():
        word = word.rstrip(punctuation)

        if (len(word) < 3):
            continue

        tickers = util.csv2dict()

        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in common_word_filters) and len(word) <= 5 and word.isalpha() and (word in tickers):
            print("OHHHHH YEAHHHH")
            if word in ticker_dict:
                ticker_dict[word].count += 1
                ticker_dict[word].bodies.append(text)
            else:
                ticker_dict[word] = Ticker(word)
                ticker_dict[word].count = 1
                ticker_dict[word].bodies.append(text)
    return


def crawl_subreddit(subreddit, hours):
    # Create praw connection


    reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                         user_agent='Comment extraction by /u/PartialSyntax')

    # iterate through latest 24 hours of submissions and all comments made on those submissions
    timestamp = int(time.time())
    # for submission in tqdm(reddit.subreddit(SUBREDDIT).new(limit=1000)):
    for submission in reddit.subreddit(SUBREDDIT).new(limit=1000):
        time_delta = timestamp - submission.created_utc
        if (time_delta > TIME_PERIOD * hours):
            break
            analyze_text(submission.title)
            analyze_text(submission.selftext)
        # Parses post comments
        submission.comments.replace_more(limit=None, threshold=0)
        # for comment in tqdm(submission.comments.list()):
        for comment in submission.comments.list():
            with open("comment.json") as file:
                data = json.load(file)
                if comment.permalink in data:
                    pass
                else:
                    faux = {comment.permalink: comment.body}
                    data.update(faux)
                    # print(data)
                    with open("comment.json", "w") as f:
                            json.dump(data,f)
                    analyze_text(comment.body)



def main(args):
    if len(args) > 1:
        try:
            crawl_subreddit("wallstreetbets", int(args[1]))
        except:
            print("ERROR: First argument must be a number")
            return
    else:   
        crawl_subreddit("wallstreetbets", 1)
    # Puts the tickers into a dict use for counting
    with open('export.txt', 'w') as f:
        print(ticker_dict, file=f)
    for ticker in ticker_dict:
        ticker_count[ticker] = ticker_dict[ticker].count
    # Prints the list of tickers in decending order
    for key, value in sorted(ticker_count.items(), key=lambda x: x[1], reverse=True):
        print(key, value)



if __name__ == '__main__':
    print("Running...")
    main(sys.argv)
    