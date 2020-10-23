global COMMON_WORDS, ALTERNATE_SPELLING, TICKERS
# list of common english words to remove
COMMON_WORDS = ["CALM","OLD","STAR","SHE","LOAN","CHAD","KNOW","BUY","SELL","PSA","NEED","FREE","JUST","SON","USD","IPO","PDT","ATH","ITM","YOLO","EPS","AUG", "CEO", "GOLD", "ALOT", "JAN", "ONCE", "EDIT", "BRO", "SU", "LIFE", "CFO", "JOB", "BIT", "TWO", "BEST", "BIG", "EOD", "HOPE", "AM", "EVER", "PUMP", "NEXT", "HE", "REAL", "WORK", "NICE", "TOO", "MAN", "LOVE", "BY", "VERY", "ANY", "SEE",
                    "NEW", "WELL", "TELL", "IT", "ONE", "POST", "ON", "TURN", "GOOD", "CAN", "HAS", "GO", "PLAY", "ELSE", "GAIN", "RUN", "INFO", "STAY", "CARE", "ALL", "AT", "PER", "DO", "ARE", "NOW", "BE", "OR", "SO", "OUT", "BEAT", "AGO", "AN", "PEAK", "LOW", "DD", "FOR", "FLAT"]
# alternate spellings of tickers
ALTERNATE_SPELLING = {
"TESLA": "TSLA",
"APPLE": "AAPL",
"NIKOLA": "NKLA",
"MICROSOFT": "MSFT",
"FACEBOOK": "FB",
"FEDEX": "FDX",
"NVIDIA": "NVDA",
"STARBUCKS": "SBUX",
"DISNEY": "DIS",
"PLEOTON": "PTON",
"DRAFT KINGS": "DKNG"
    }

    # Holds all of the tickers
TICKERS = open("symbols.txt").read().splitlines()