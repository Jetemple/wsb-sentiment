import config
import praw
import time
import json
import yfinance as yf

# reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, user_agent='Comment extraction by /u/rizir')

# start = time.time()


# for submission in reddit.subreddit("wallstreetbets").new(limit=10):
#     # print(submission.created_utc)
#     # print(time.time()-1595415600)
#     submission.comments.replace_more(limit=None, threshold=0)
#     for comment in submission.comments.list():
#         print("here")
#     # print(time.time())
#     # print(time.time()-submission.created_utc) #how long ago this submission was created


# print("Praw time: ", time.time()-start)
# checkpoint = time.time()
# tsla = yf.Ticker("TSLA").info
# print(tsla["longName"])
# try:
#     # tsla = yf.Ticker("fuck")
   
# except:
#     print("LMAO")

# checkpoint = time.time() - checkpoint
# print("YF time", checkpoint)

tsla = yf.Ticker("TSLA").info
print(tsla["longName"])

faux = {"TSLA": tsla["longName"]}
# faux = {"r"}

with open("cache.json", "r+") as file:
    data = json.load(file)
    data.update(faux)
    file.seek(0)
    json.dump(data,file)
