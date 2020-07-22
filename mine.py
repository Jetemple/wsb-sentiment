import csv
import praw
import time
import os
import logging
import sys
from string import punctuation
sys.path.insert(0, 'vaderSentiment/vaderSentiment')
from vaderSentiment import SentimentIntensityAnalyzer


#contains client_id and client_secret used to connect
import config

file1 = open("myfile.txt","w")

sys.stdout = file1

# TIME_PERIOD						= 60 * 60 * 4 * 1
TIME_PERIOD						= 60 * 20

SUBREDDIT						= 'wallstreetbets'
STOCK_SPECIFIC_METION_WEIGHT 	= 5
STOCK_POST_MENTION_WEIGHT 		= 3
STOCK_DEFAULT_WEIGHT			= 1

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger = logging.getLogger('prawcore')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

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
      self.sentiment = 0 # 0 is neutral

   def analyze_sentiment(self):
      analyzer = SentimentIntensityAnalyzer()
    #   print("HERE")
    #   print(self)
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



#list of common english words to remove
common_word_filters=["GOLD", "ALOT", "JAN", "ONCE", "EDIT", "BRO", "SU", "LIFE", "CFO", "JOB", "BIT", "TWO", "BEST", "BIG", "EOD", "HOPE", "AM", "EVER", "PUMP", "NEXT", "HE", "REAL", "WORK", "NICE", "TOO", "MAN", "LOVE", "BY", "VERY", "ANY", "SEE", "NEW", "WELL", "TELL", "IT", "ONE", "POST", "ON", "TURN", "GOOD", "CAN", "HAS", "GO", "PLAY", "ELSE", "GAIN", "RUN", "INFO", "STAY", "CARE", "ALL", "AT", "PER", "DO", "ARE", "NOW", "BE", "OR", "SO", "OUT", "BEAT", "AGO", "AN", "PEAK", "LOW", "DD", "FOR", "FLAT"]
common_word_translations={"AVIS" : "CAR", "SPOTIFY" : "SPOT", "TESLA" : "TSLA", "Lockheed" : "LMU", "MICRON" : "MU", "SHOPIFY" : "SHOP", "DISNEY" : "DIS", "Boeing" : "BA", "NETFLIX" : "NFLX", "APPLE" : "AAPL", "INTEL" : "INTC", "PELOTON" : "PTON", "PELETON" : "PTON", "GOOGLE" : "GOOG", "STARBUCKS" : "SBUX"}
word_counts={}
stocks={}
specific_stocks={}

#Load base list of stock symbols from all csv files in cwd
#the first column must be the stock symbol
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".csv"): 
        # print("Loading {}...".format(filename))
        
        with open(filename, mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                Ticker(rows[0])
                stocks[Ticker(rows[0]).ticker] = Ticker(rows[0])
print("HERE")
print(stocks)

#analyze a blob of text, increment counts in stock dictionary
#add new entries for any words thats start with a $
def analyze_text(text, value=STOCK_DEFAULT_WEIGHT):
    for word in text.split():
        word=word.upper()
        word = word.rstrip(punctuation)

        
        if (len(word)<3):
            continue
            
        if ( (word.isalnum()) or ( (word[0] is "$") and (word[1:].isalpha()) )):
            if word in stocks and (word not in common_word_filters):
                
                # print(stocks[word].ticker)
                stocks[word].bodies.append(text)
                stocks[word].count = stocks[word].count + 1
                # print("FUCK YEAHHHH")
                # print(stocks[word].count)
                # print(stocks[word].bodies)

            if word in word_counts:
                word_counts[word] += value
            else:
                word_counts[word] = value


# print("Crawling subreddit[{}] for all posts/comments within the last {} seconds".format(SUBREDDIT, TIME_PERIOD))

#Create praw connection	
reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, user_agent='Comment extraction by /u/rizir')

#iterate through latest 24 hours of submissions and all comments made on those submissions

timestamp	= int(time.time())

for submission in reddit.subreddit(SUBREDDIT).new(limit=1000):
    time_delta=timestamp - submission.created_utc

    if (time_delta > TIME_PERIOD):
        break

    print("Title:\t", submission.title)
    print("ID:\t", submission.id)
    print("Comments:\t", submission.num_comments)
    print("Age:\t", time_delta)

    analyze_text(submission.title, value=STOCK_POST_MENTION_WEIGHT)
    analyze_text(submission.selftext, value=STOCK_POST_MENTION_WEIGHT)

    #submission.comments.replace_more(limit=None, threshold=0)
    if submission.num_comments > 500:
        print("Getting more comments (", submission.num_comments, "), this may take a while...")
    submission.comments.replace_more(limit=None, threshold=0)
    
    for comment in submission.comments.list():
        print("\t", comment.id)
        analyze_text(comment.body)

    print()

final_stocks={}

for stock in stocks:
    if(stock == "TSLA"):
        print("FUCK")
        print(stocks[stock].count)
    if((stocks[stock].count) > 0):
        Ticker.analyze_sentiment(stocks[stock])
        print("=====================================")
        print(stock)
        print(stocks[stock].bodies)
        print("Bearish:", stocks[stock].bearish, "%")
        print("Bullish:", stocks[stock].bullish, "%")
        print("Neutral:", stocks[stock].neutral, "%")
    # print(stocks[stock].count)
    # if stock.count is not 0:
    #     final_stocks[stock] = stock
    #     print(final_stocks[stock].count)
    # print(stock)
    

file1.close()

