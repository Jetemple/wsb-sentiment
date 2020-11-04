import config
import time
import crawler as crawl

def main():
    # pickup = crawl_subreddit("wallstreetbets")
    pickup = time.time()
    crawl.crawl_subreddit(SUBREDDIT)
    # crawl.getHistory(pickup)


if __name__ == "__main__":
    TIME_PERIOD = 60 * 60 * 60# How far you want to go back in the subreddit
    SUBREDDIT = 'wallstreetbets'
    a = time.time()
    main()
    print(time.time()-a)