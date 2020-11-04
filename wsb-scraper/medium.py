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

import sentiment
import globalLists as gl
# gl.init()

BASE_URL = config.BASE_URL


def getLargeThread(threadId, cutoff):
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
        sentiment.analyze_text(d)
        count += 1
        cutoff = d['created_utc']
    if(count == 20000):
        return cutoff
    return -1

# May Be depricated
def getPushshift(thread):
    try:
        url = "https://api.pushshift.io/reddit/comment/search/?link_id="+thread+"&limit=100000"
        print(url)
        r = requests.get(url)
        data = r.json()
        for d in data['data']:
            a = time.time()
            sentiment.analyze_text(d)
            print(time.time()-a)
    except Exception as e:
        print(e)

def addPost(post):
    # Initial Values
    ticker = "N/A"
    isDict = type(post) == dict
    title = post.get("title")if isDict else post.title

    # Finds the ticker in the title
    for word in title.split():
        print(word)
        word = word.strip(punctuation)
        word = word.upper()
        if gl.ALTERNATE_SPELLING.get(word) != None:
            word = gl.ALTERNATE_SPELLING.get(word)
            print(word)
        if (len(word) < 2):
            continue
        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in gl.COMMON_WORDS) and len(word) <= 5 and word.isalpha() and (word.upper() in gl.TICKERS):
            ticker = word
            break

    if isDict:
        data = {
        "post_id" : post.get("id"),
        "post_date" : post.get("created_utc"),
        "num_comments" : post.get("num_comments"),
        "score" : post.get("score"),
        "upvote_ratio" : post.get("upvote_ratio") if post.get("upvote_ratio") != None else "-1",
        "guildings" : post.get("guildings") if post.get("guildings") != None else 0,
        "flair" : post.get("link_flair_text") if post.get("link_flair_text") != None else "none",
        "author" : post.get("author"),
        "ticker" : ticker,
        "title" : title,
        "body" : post.get("selftext") if post.get("selftext") != None else " ",
        "sentiment" : "TODO"
        }
    else:
        print("PRAW")
        numAwards = len(post.all_awardings)
        data = {
        "post_id" : post.id,
        "post_date" : int(post.created_utc),
        "num_comments" : post.num_comments,
        "score" : post.score,
        "upvote_ratio" : post.upvote_ratio,
        "guildings" : numAwards,
        "flair" : post.link_flair_text if post.link_flair_text != None else "None",
        "author" : post.author,
        "ticker" : ticker,
        "title" : post.title,
        "body" : post.selftext,
        "sentiment" : "TODO"
        }
    print(data)
    r = requests.post(url = BASE_URL+"/posts", data = data)
    

def largeLoop(large_threads):
    print("Start Large Threads")
    for t in large_threads:
        print(t)
        cutoff = 0
        while(cutoff != -1):
            cutoff = getLargeThread(t,cutoff)

def getHistory(pickup):
    utc=time.time()-172800 #Pushift.io collects comment data on posts older than 48 hours 
    # utc=1588197864.2323
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