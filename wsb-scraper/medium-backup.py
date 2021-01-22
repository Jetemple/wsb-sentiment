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

import sentiment as s
import globalLists as gl

BASE_URL = config.BASE_URL
SUBREDDIT = config.SUBREDDIT
TIME_PERIOD = config.TIME_PERIOD
large_threads=[]

def addPost(post):
    # Initial Values
    ticker = "N/A"
    isDict = type(post) == dict
    title = post.get("title")if isDict else post.title

    # Finds the ticker in the title
    for word in title.split():
        word = word.strip(punctuation)
        word = word.upper()
        if gl.ALTERNATE_SPELLING.get(word) != None:
            word = gl.ALTERNATE_SPELLING.get(word)
        if (len(word) < 2):
            continue
        # Does word fit the ticker criteria
        if word.isupper() and len(word) != 1 and (word.upper() not in gl.COMMON_WORDS) and len(word) <= 5 and word.isalpha() and (word.upper() in gl.TICKERS):
            ticker = word
            break

    if isDict:
        print("PUSH")
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
    r = requests.post(url = BASE_URL+"/posts", data = data)
    
def addComment(comment):
    # BASE_URL = "http://localhost:3000/comments"
    isDict = type(comment) == dict
    # awards = ''
    if(isDict):
        text = comment['body']
        id = comment['id']
        time = comment['created_utc']
        score = comment['score']
        parent = comment['parent_id']
        if parent.startswith("t"):
            parent = parent[3:]
    else:
        text = comment.body
        time = comment.created_utc
        id = comment.id
        score = comment.score
        parent = comment.link_id[3:]
        # awards = item.all_awardings

    # for word in text.split():
    #     word = word.strip(punctuation)
        
    #     # Tickers of len<2 do not exist
    #     if (len(word) < 2):
    #         continue

    #     # Does word fit the ticker criteria
    #     if word.isupper() and len(word) != 1 and (word.upper() not in gl.COMMON_WORDS) and len(word) <= 5 and word.isalpha() and (word.upper() in gl.TICKERS):
    #         # Checks to see if the ticker has been cached.
    #         # url = "http://localhost:3000/id/" + id
    #         r = requests.get(url= BASE_URL + "/id/" + id)
    #         if(r.status_code == 200):
    #             continue
    #         sentiment = s.analyze_sentiment(text)
    #         # print(score)
    #         data = {
    #             "comment_id" : id,
    #             "comment_date" : time,
    #             "ticker" : word,
    #             "parent_post" : parent,
    #             "body" : text,
    #             "score" : score,
    #             "sentiment" : sentiment
    #             }
    #         r = requests.post(url = BASE_URL+"/comments", data = data)
    r = requests.get(url= BASE_URL + "/id/" + id)
    # if(r.status_code == 200):
    #     continue
    sentiment = s.analyze_sentiment(text)
    # print(score)
    data = {
        "comment_id" : id,
        "comment_date" : time,
        "ticker" : "TEST",
        "parent_post" : parent,
        "body" : text,
        "score" : score,
        "sentiment" : sentiment
        }
    r = requests.post(url = BASE_URL+"/comments", data = data)