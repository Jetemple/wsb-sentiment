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

<<<<<<< HEAD

TIME_PERIOD = 60 * 60 * 6 #How far back to scrape in UNIX time
SUBREDDIT = 'wallstreetbets'
STOCK_SPECIFIC_METION_WEIGHT = 5
STOCK_POST_MENTION_WEIGHT = 3
STOCK_DEFAULT_WEIGHT = 1
=======
TIME_PERIOD = 60 * 60 # How far you want to go back in the subreddit
SUBREDDIT = 'wallstreetbets'
>>>>>>> origin/master

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

# Checks to see if there are tickers in the word
def analyze_text(text):
    for word in text.split():
        word = word.rstrip(punctuation)

        if (len(word) < 3):
            continue

        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in common_word_filters) and len(word) <= 5 and word.isalpha():
            with open("cache.json") as file, open("false-positives.json") as file2:
                data = json.load(file)
                data2 = json.load(file2)
                # Checks to see if the ticker has been cached.
                if (word not in data) and (word not in data2):
                    try: # Add ticker to cache 
                        company = yf.Ticker(word).info["longName"]
                        add = {word : company}
                        data.update(add)
                        with open("cache.json", "w") as f:
                            json.dump(data,f)
                    except Exception as e:
                        if(word not in data2):
                            add = {word : str(e)}
                            data2.update(add)
                            with open("false-positives.json", "w") as f:
                                json.dump(data2,f)
                        continue
            if (word in data) and (word in ticker_dict):
                ticker_dict[word].count += 1
                ticker_dict[word].bodies.append(text)
            elif word in data:
                ticker_dict[word] = Ticker(word)
                ticker_dict[word].count = 1
                ticker_dict[word].bodies.append(text)           
    return ticker_dict


def crawl_subreddit(subreddit):
    # Create praw connection
    reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                         user_agent='Comment extraction by /u/PartialSyntax')

    # iterate through latest 24 hours of submissions and all comments made on those submissions
    timestamp = int(time.time())
    for submission in reddit.subreddit(SUBREDDIT).new(limit=1000):
        time_delta = timestamp - submission.created_utc
        if (time_delta > TIME_PERIOD):
            break
        ticker_dict = analyze_text(submission.title)
        ticker_dict = analyze_text(submission.selftext)
        # Parses post comments
        submission.comments.replace_more(limit=None, threshold=0)
        for comment in submission.comments.list():
            ticker_dict = analyze_text(comment.body)


crawl_subreddit("wallstreetbets")
count = {}
for ticker in ticker_dict:
    count[ticker] = ticker_dict[ticker].count


for key, value in sorted(count.items(), key=lambda x: x[1], reverse=True):
    print(key, value)