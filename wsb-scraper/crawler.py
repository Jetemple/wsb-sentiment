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

import sentiment
import globalLists as gl
import medium as m

BASE_URL = config.BASE_URL
SUBREDDIT = config.SUBREDDIT
TIME_PERIOD = config.TIME_PERIOD
large_threads=[]

def crawl_subreddit(subreddit):
    try:
        # Create praw connection
        reddit = praw.Reddit(client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRETS,
                            user_agent='Comment extraction by /u/PartialSyntax')
        # iterate through latest 24 hours of submissions and all comments made on those submissions
        timestamp = int(time.time())
        for submission in reddit.subreddit(SUBREDDIT).new(limit=1000):
            time_delta = timestamp - submission.created_utc
            if (time_delta > TIME_PERIOD):
                break
            # seen = dbm.checkPost(submission.id)
            # if (submission.num_comments<1000):
            #     print(submission.num_comments)
            #     sentiment.analyze_text(submission)
            # count = dbm.getCommentCount(submission)
            # if(seen and count == submission.num_comments):
            #     continue
                            
            # Parses post comments
            m.addPost(submission)
            if (submission.num_comments > 999):
                large_threads.append(submission.id)
                print("LARGE THREAD ALERT")
                continue    
            submission.comments.replace_more(limit=999)
            for comment in submission.comments.list():
                if(type(comment)==praw.models.reddit.more.MoreComments):
                    print("MORE_COMMENTS")
                    continue
                else:  
                    m.addComment(comment)
            last_time = submission.created_utc
            # try:
            #     for comment in submission.comments.list():
                    # if(type(comment)==praw.models.reddit.more.MoreComments):
                    #     continue
                    # if (submission.num_comments > 999):
                    #     large_threads.append(submission.id)
                    #     print(submission.id)
            #             break
            #         else:
            #             m.addComment(comment)

            # except Exception as e:
            #     print(e)
        print("=============================RUNNING LARGE THREAD LOOP================================")
        # largeLoop(large_threads)
        return last_time
    except Exception as e:
        print(e)
        pass


def getPushshift(threadId):
    # url = "jq4o82"
    cutoff = 0
    while(True):
        url = "https://api.pushshift.io/reddit/comment/search/?link_id="+threadId+"&limit=100000"
        if (cutoff != 0):
            url = str(url) + "&before="+str(cutoff)
        print(url)
        r = requests.get(url)
        # print(r)
        data = r.json()
        count = 0
        for d in data['data']:
            print("working")
            # print(d['id'])
            m.addComment(d)
            count += 1
            cutoff = d['created_utc']
        if(count != 20000):
            return
    return 

def largeLoop(large_threads):
    print("Start Large Threads")
    for t in large_threads:
        getPushshift(t)

def getHistory():
    utc=time.time()-(60 * 60 * 72) #Pushift.io collects comment data on posts older than 48 hours 
    a=utc
    dif = utc - (60 * 60 * 24 * 30)
    # dif = utc - (60*60*24*7)
    print(dif)
    print(utc)
    unixTime=str(utc)[:str(utc).index('.')]
    while(dif<utc):
        try:
            url ="https://api.pushshift.io/reddit/submission/search/?subreddit=wallstreetbets&sort=desc&after=0&before="+unixTime+"&size=1000&user_removed=false&mod_removed=false"
            print(url)
            r = requests.get(url)

            # print(url)
            data = r.json()
            for d in data['data']:
                if(d.get('removed_by_category')==None):
                    m.addPost(d)
                    # large_threads.append(d.get('id'))
                    # print(d.get('id'))
                    getPushshift(d.get('id'))
                    # print(d['id'])
                    # print(d.get('removed_by_category'))
                    # 
                # print(d)
                # print(datetime.utcfromtimestamp(utc).strftime('%Y-%m-%d %H:%M:%S'),d['created_utc'],d['title'])
                unixTime=str(d['created_utc'])
                utc=d['created_utc']
                # print(datetime.utcfromtimestamp(utc).strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            print(e)

        
    print(time.time()-a)
