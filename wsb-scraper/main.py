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

# TIME_PERIOD = 60 * 60 * 1000# How far you want to go back in the subreddit
# SUBREDDIT = 'wallstreetbets'


a = time.time()

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
        word = word.rstrip(punctuation)
        
        # Tickers of len<2 do not exist
        if (len(word) < 3):
            continue
 
        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in common_word_filters) and len(word) <= 5 and word.isalpha() and (word.upper() in tickers):
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
            analyze_text(submission)
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
                    analyze_text(comment)
        except Exception as e:
            print(e)
        last_time = submission.created_utc
    return last_time


        

def getLarge(threadId, cutoff):
    url = "https://api.pushshift.io/reddit/comment/search/?link_id="+threadId+"&limit=100000"
    print(url)
    if (cutoff != 0):
        url = str(url) + "&before="+str(cutoff)
    # print(url)
    r = requests.get(url)
    # print(r)
    data = r.json()
    count = 0
    for d in data['data']:
        # print(d['id'])
        analyze_text(d)
        count += 1
        cutoff = d['created_utc']
    if(count == 20000):
        return cutoff
    return -1
def getPushshift(thread):
    try:
        url = "https://api.pushshift.io/reddit/comment/search/?link_id="+thread+"&limit=100000"
        print(url)
        r = requests.get(url)
        data = r.json()
        for d in data['data']:
            a = time.time()
            analyze_text(d)
            print(time.time()-a)
    except Exception as e:
        print(e)

def addPost(this):
    BASE_URL = "http://localhost:3000/posts"
    ticker = "N/A"
    guildings = "none"
    upvote_ratio = "0.0"

    if this.get("upvote_ratio") != None:
        upvote_ratio = this.get("upvote_ratio")
    
    if this.get("guildings") != None:
        guildings = this.get("guildings")
    for word in this.get("title").split():
        word = word.rstrip(punctuation)
        if (len(word) < 3):
            continue
 
        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in common_word_filters) and len(word) <= 5 and word.isalpha() and (word.upper() in tickers):
            ticker = word
            break

    for word in this.get("selftext").split():
        if(ticker != "NONE"):
            break
        word = word.rstrip(punctuation)
        if (len(word) < 3):
            continue
 
        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in common_word_filters) and len(word) <= 5 and word.isalpha() and (word.upper() in tickers):
            ticker = word
            break
    data = {
	"post_id" : this.get("id"),
	"post_date" : this.get("created_utc"),
	"num_comments" : this.get("num_comments"),
	"score" : this.get("score"),
	"upvote_ratio" : this.get("upvote_ratio"),
	"guildings" : guildings,
	"flair" : this.get("link_flair_text"),
	"ticker" : ticker,
	"title" : this.get("title"),
	"body" : this.get("selftext"),
	"sentiment" : "TODO"
    }
    r = requests.post(url = BASE_URL, data = data)


def getHistory(pickup):
    # utc=time.time()-172800 #Pushift.io collects comment data on posts older than 48 hours 
    utc=1588197864.2323
    # utc=pickup
    a=utc
    dif = utc - 31557600
    # dif = utc - (60*60*24*7)
    print(dif)
    print(utc)
    utcS=str(utc)[:str(utc).index('.')]
    while(dif<utc):
        try:
            url ="https://api.pushshift.io/reddit/submission/search/?subreddit=wallstreetbets&sort=desc&after=0&before="+utcS+"&size=1000&user_removed=false&mod_removed=false"
            r = requests.get(url)

            print(url)
            data = r.json()
            for d in data['data']:
                cutoff = 0
                if(d.get('removed_by_category')==None):
                    addPost(d)
                    # large_threads.append(d.get('id'))
                    # print(d.get('id'))
                    # getPushshift(d.get('id'))
                    # print(d['id'])
                    # print(d.get('removed_by_category'))
                    # 
                # print(d)
                # print(datetime.utcfromtimestamp(utc).strftime('%Y-%m-%d %H:%M:%S'),d['created_utc'],d['title'])
                utcS=str(d['created_utc'])
                utc=d['created_utc']
                # print(datetime.utcfromtimestamp(utc).strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            print(e)

        
    print(time.time()-a)

def largeLoop():
    print("Start Large Threads")
    for t in large_threads:
        print(t)
        cutoff = 0
        while(cutoff != -1):
            cutoff = getLarge(t,cutoff)

def main():
    # pickup = crawl_subreddit("wallstreetbets")
    pickup = time.time()
    getHistory(pickup)
    largeLoop()


if __name__ == "__main__":
    TIME_PERIOD = 60 * 60 * 1000# How far you want to go back in the subreddit
    SUBREDDIT = 'wallstreetbets'
    a = time.time()
    main()
    print(time.time()-a)