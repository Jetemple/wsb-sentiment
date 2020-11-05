# WallStreetBets Sentiment 

This tool is used to parse all of the comments on WSB in the past X time. Counts the tickers and their occurrence count, then presents if WSB is bullish or bearish or neutral on said ticker. (Using a custom version of VaderSentiment)

## TODO List 

- [ ] Improve VADER Sentiment
- [ ] Add Changelog
- [ ] Create Web App 
- [ ] Create setup.py
  
   - [ ] Add init SQL scripts 
- [ ] Handle "MoreComments"
- [x] Add Award Count
- [x] Add comments to database

## Thoughts
* What submissions should I go throgh? 
  * New/Hot/Top/Controversial/Guilded

## Issues 
* Potential for multiple tickers within comments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites
* Docker-compose 
* Python 3.8.3

```
cd wsb-scraper
pip install -r requirements.txt
```

### Running app 
```
# Starts MySQL DB and Node server 
docker-compose up --build
# Run Scraper in other terminal window
cd wsb-scraper
python main.py
```


## Built With

* ***Future*** : [VaderSentiment](https://github.com/cjhutto/vaderSentiment) - Used to determine if comment of ticker is Bullish or Bearish. *(Tweaked with personal rules)*
* MySQL

## Contributing

Fork this repo and merge into master.

*Will update contributing rules once versioning is decided*

## Versioning

***TBD***

## Authors

* **Jetemple** - *Sole work* 
  
See also the list of [contributors](https://github.com/Jetemple/wsb-sentiment/contributors) who participated in this project.

## Acknowledgments

* Thank you WSB for letting me pick your brains.
  
  ![alt text](https://i.imgur.com/JVYC0Em.png)

