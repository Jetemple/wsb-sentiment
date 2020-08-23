# WallStreetBets Sentiment 

This tool is used to parse all of the comments on WSB in the past X time. Counts the tickers and their occurrence count, then presents if WSB is bullish or bearish or neutral on said ticker. (Using a custom version of VaderSentiment)

## TODO List 

- [ ] Improve VADER Sentiment
- [ ] Add Changelog
- [ ] Create Web App 
- [ ] Create setup.py
- [ ] Handle "MoreComments"
- [x] Add comments to database

## Issues 
* ~~PRAW limited to last 1000 items~~.
* Potential for multiple tickers within comments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

```
pip install -r requirements.txt
```


## Built With

* ***Future*** : [VaderSentiment](https://github.com/cjhutto/vaderSentiment) - Used to determine if comment of ticker is Bullish or Bearish. *(Tweaked with personal rules)*
* SQLITE3

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

