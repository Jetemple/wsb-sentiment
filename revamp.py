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

sys.path.insert(0, 'vaderSentiment/vaderSentiment')
from vaderSentiment import SentimentIntensityAnalyzer

TIME_PERIOD = 60 * 60 * 4 # How far you want to go back in the subreddit
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


# list of common english words to remove
common_word_filters = ["AUG", "CEO", "GOLD", "ALOT", "JAN", "ONCE", "EDIT", "BRO", "SU", "LIFE", "CFO", "JOB", "BIT", "TWO", "BEST", "BIG", "EOD", "HOPE", "AM", "EVER", "PUMP", "NEXT", "HE", "REAL", "WORK", "NICE", "TOO", "MAN", "LOVE", "BY", "VERY", "ANY", "SEE",
                       "NEW", "WELL", "TELL", "IT", "ONE", "POST", "ON", "TURN", "GOOD", "CAN", "HAS", "GO", "PLAY", "ELSE", "GAIN", "RUN", "INFO", "STAY", "CARE", "ALL", "AT", "PER", "DO", "ARE", "NOW", "BE", "OR", "SO", "OUT", "BEAT", "AGO", "AN", "PEAK", "LOW", "DD", "FOR", "FLAT"]

ticker_dict = {} # Holds all of the tickers
tickers = open("symbols.txt").read().splitlines()# Holds all of the tickers

# Checks to see if there are tickers in the word
def analyze_text(text):
    for word in text.split():
        word = word.rstrip(punctuation)

        if (len(word) < 3):
            continue

        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in common_word_filters) and len(word) <= 5 and word.isalpha() and (word.upper() in tickers):
            # Checks to see if the ticker has been cached.
            if (word in ticker_dict):
                ticker_dict[word].count += 1
                ticker_dict[word].bodies.append(text)
            else:
                ticker_dict[word] = Ticker(word)
                ticker_dict[word].count = 1
                ticker_dict[word].bodies.append(text)           
    return ticker_dict


def crawl_subreddit(subreddit):
    a = time.time()
    # Create praw connection
    reddit = praw.Reddit(client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRETS,
                         user_agent='Comment extraction by /u/PartialSyntax')
    b = time.time()
    # print(b-a ,"time to connect to reddits")
    a = time.time()
    # iterate through latest 24 hours of submissions and all comments made on those submissions
    with open("cache-posts.json") as file:
        data = json.load(file)
        timestamp = int(time.time())
        aa = time.time()
        for submission in reddit.subreddit(SUBREDDIT).new(limit=1000):
            time_delta = timestamp - submission.created_utc
            if (time_delta > TIME_PERIOD):
                break
            if submission.id not in data:
                ticker_dict = analyze_text(submission.title)
                ticker_dict = analyze_text(submission.selftext)
                add = {submission.id : submission.num_comments}
                data.update(add)
                with open("cache-posts.json", "w") as f:
                        json.dump(data,f)
            # print(submission.num_comments)
            # if submission.num_comments > int(data[submission.id]):
            #     break

            
            # Parses post comments
            submission.comments.replace_more(limit=None, threshold=0)
            for comment in submission.comments.list():
                if comment.id not in data:
                    # print("test")
                    add = {comment.id : "0"}
                    data.update(add)
                    with open("cache-posts.json", "w") as f:
                            json.dump(data,f)
                    ticker_dict = analyze_text(comment.body)
    #         b = time.time()
    #         print(b-aa ,"time to parse go through one post")
    # b = time.time()
    # print(b-a ,"time to parse comments")
                


crawl_subreddit("wallstreetbets")
count = {}
for ticker in ticker_dict:
    count[ticker] = ticker_dict[ticker].count


for key, value in sorted(count.items(), key=lambda x: x[1], reverse=True):
    print(key, value)
b = time.time()
print(b-a)