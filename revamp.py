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


TIME_PERIOD = 60 * 60 # How far you want to go back in the subreddit
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
common_word_filters = ["SON","USD","IPO","PDT","ATH","ITM","YOLO","EPS","AUG", "CEO", "GOLD", "ALOT", "JAN", "ONCE", "EDIT", "BRO", "SU", "LIFE", "CFO", "JOB", "BIT", "TWO", "BEST", "BIG", "EOD", "HOPE", "AM", "EVER", "PUMP", "NEXT", "HE", "REAL", "WORK", "NICE", "TOO", "MAN", "LOVE", "BY", "VERY", "ANY", "SEE",
                       "NEW", "WELL", "TELL", "IT", "ONE", "POST", "ON", "TURN", "GOOD", "CAN", "HAS", "GO", "PLAY", "ELSE", "GAIN", "RUN", "INFO", "STAY", "CARE", "ALL", "AT", "PER", "DO", "ARE", "NOW", "BE", "OR", "SO", "OUT", "BEAT", "AGO", "AN", "PEAK", "LOW", "DD", "FOR", "FLAT"]

ticker_dict = {} # Holds all of the tickers
tickers = open("symbols.txt").read().splitlines()# Holds all of the tickers

# Checks to see if there are tickers in the word
def analyze_text(text, id, time):
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
            dbm.addTicker(word)
            dbm.addComment(id,time,word)
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
            # if submission.id not in data:
            # if not dbm.checkComment(submission.id):
            #     ticker_dict = analyze_text(submission.title, submission.id, submission.created_utc)
            #     ticker_dict = analyze_text(submission.selftext, submission.id, submission.created_utc)
            
             # dbm.addPost(submission.id, submission.num_comments, submission.id)
            ticker_dict = analyze_text(submission.title, submission.id, submission.created_utc)
            ticker_dict = analyze_text(submission.selftext, submission.id, submission.created_utc)
            if not(dbm.addPost(submission.id, submission.num_comments, submission.created_utc)):
                count = dbm.getCommentCount(submission)
                if(count == submission.num_comments):
                    print("Skipped!!!!")
                    continue
                         
            # Parses post comments
            # submission.comments.replace_more(limit=None, threshold=0)
            for comment in submission.comments.list():
                if isinstance(comment, MoreComments):
                    continue
            #     # if comment.id not in data:
            #     # print("test")
            #     # add = {comment.id : "0"}
            #     # data.update(add)
            #     # with open("cache-posts.json", "w") as f:
            #     #         json.dump(data,f)
                if(dbm.checkComment(comment.id)):
                    ticker_dict = analyze_text(comment.body, comment.id, comment.created_utc)
                
    #         b = time.time()
    #         print(b-aa ,"time to parse go through one post")
    # b = time.time()
    # print(b-a ,"time to parse comments")
                


crawl_subreddit("wallstreetbets")
count = {}
for ticker in ticker_dict:
    ticker_dict[ticker].analyze_sentiment()
    # print(ticker_dict[ticker].pos_count)
    count[ticker] = ticker_dict[ticker].count

print("Stock \t Count \t Bullish \t Neutral \t Bearish")
for key, value in sorted(count.items(), key=lambda x: x[1], reverse=True):
    # print("Bullish", ticker_dict[key].bullish)
    # print("Neutral", ticker_dict[key].neutral)
    # print("Bearish", ticker_dict[key].bearish)
    # print(key, value , ticker_dict[key].bullish , ticker_dict[key].neutral , ticker_dict[key].bearish)
    # print(key, "\t", value , "\t",ticker_dict[key].pos_count ,len(ticker_dict[key].bodies) ,ticker_dict[key].bullish , "\t\t", ticker_dict[key].neutral , "\t\t", ticker_dict[key].bearish)
    print(key, "\t", value , "\t" ,ticker_dict[key].bullish , "\t\t", ticker_dict[key].neutral , "\t\t", ticker_dict[key].bearish)
b = time.time()
print(b-a)