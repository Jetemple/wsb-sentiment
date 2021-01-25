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
    ticker = s.findTicker(title)
    if ticker == "N/A":
        body = post.get("selftext") if isDict else post.selftext
        ticker = s.findTicker(body)

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
        parent_post = comment['link_id']
        parent_post = parent_post[3:]
        parent_comment = "t_0 " if comment['parent_id'] == parent_post else comment['parent_id']
        # if parent_post.startswith("t"):
        #     parent_post = parent_post[3:]
        author = comment['author']
    else: 
        text = comment.body
        time = comment.created_utc
        time = str(time).rstrip('.0')
        id = comment.id
        score = comment.score
        parent_post = comment.link_id[3:]
        # parent_comment = "top_level" if comment.link_id[3:] == comment.parent_id[3:] else comment.parent_id[3:]
        parent_comment = "t_0" if comment.link_id == comment.parent_id else comment.parent_id
        author = comment.author
        # awards = item.all_awardings
    ticker = s.findTicker(text)
    # r = requests.get(url= BASE_URL + "/id/" + id)
    # sentiment = s.analyze_sentiment(text)
    sentiment = "Todo"
    data = {
        "comment_id" : id,
        "comment_date" : time,
        "ticker" : ticker,
        "parent_post" : parent_post,
        "parent_comment" : parent_comment,
        "body" : text,
        "score" : score,
        "sentiment" : sentiment,
        "author" : author   
        }
    r = requests.post(url = BASE_URL+"/comments", data = data)