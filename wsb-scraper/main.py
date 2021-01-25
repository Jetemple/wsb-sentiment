import config
import time
import crawler as crawl

def main():
    # pickup = crawl_subreddit("wallstreetbets")
    # crawl.crawl_subreddit(SUBREDDIT)
    crawl.getHistory()

if __name__ == "__main__":
    SUBREDDIT = 'wallstreetbets'
    a = time.time()
    main()
    print(time.time()-a)