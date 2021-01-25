global COMMON_WORDS, ALTERNATE_SPELLING, TICKERS
# list of common english words to remove
COMMON_WORDS = ["CALM","OLD","STAR","SHE","LOAN","CHAD","KNOW","BUY","SELL","PSA","NEED","FREE","JUST","SON","USD","IPO","PDT","ATH","ITM","YOLO","EPS","AUG", "CEO", "GOLD", "ALOT", "JAN", "ONCE", "EDIT", "BRO", "SU", "LIFE", "CFO", "JOB", "BIT", "TWO", "BEST", "BIG", "EOD", "HOPE", "AM", "EVER", "PUMP", "NEXT", "HE", "REAL", "WORK", "NICE", "TOO", "MAN", "LOVE", "BY", "VERY", "ANY", "SEE", "NEW", "WELL", "TELL", "HAIL", "IT", "ONE", "POST", "ON", "TURN", "GOOD", "CAN", "HAS", "GO", "PLAY", "ELSE", "GAIN", "RUN", "INFO", "STAY", "CARE", "ALL", "AT", "PER", "DO", "ARE", "NOW", "BE", "OR", "SO", "OUT", "BEAT", "AGO", "AN", "PEAK", "LOW", "DD", "FOR", "MAIN", "SIZE", "JOBS", "DOG", "BOSS", "OPEN", "HI", "WOW", "KIDS", "WANT", "HOLD", "SUB", "MOON", "TRUE", "CASH", "PLAN", "TERM", "DUDE", "DEEP", "AWAY", "FUND", "RIDE", "COST", "MUST", "LIVE", "HUGE", "THO", "EAT", "RH", "FUN", "CAR", "COST", "FDS", "HOME", "VS", "PRO", "PAYS", "LAKE", "PLUS", "GLAD", "IMO", "KIDS", "WOW", "MAX", "VS", "NEAR", "SAVE", "TECH", "EV", "FAST", "SAFE", "PICK", "PM", "HOME", "MOM", "RC", "FDS", "GROW", "STEP", "DM", "PT", "TD", "SHIP", "HACK", "EARN", "LEG", "SHIP", "RAMP", "IVE" , "MOD", "JACK", "NET", "TEAM", "UK", "SALT", "PRO", "ROCK", "DUST", "GOLF", "APPS", "CUZ", "IRS", "ROLL", "LAWS", "CUT", "KEY", "MARK", "FAT", "FAN", "IQ", "TA", "DDS", "WISH", "FR", "MASS", "CUZ", "ROLL", "SELF", "BC", "PPL", "FLY", "FILL", "CUT", "ONTO", "EYE", "IRS", "FAM", "TOWN", "UK", "CRY", "HES", "EYES", "PRO", "BUD", "FB", "CARS", "FORM", "MID", "EARN", "FAT", "AMP", "JACK", "ROCK", "BILL", "DDS", "MARK", "MOD", "BLUE", "DEF", "LAWS", "KEY", "AUTO", "LEND", "FIVE", "LEAP", "LEAD", "TIP", "MIN", "NERD", "SITE", "MEN", "EXP", "PAYS", "TEN", "FAN", "LAZY", "LAND", "TY", "WOOD", "BOUT", "RARE", "CC", "AIR", "EH", "TDA", "TRIP", "SMH", "TV", "CAKE", "IQ", "SKY", "FOUR", "ROAD", "PIN", "SIX", "JOE", "TA", "HA", "BAR", "FIX", "FR", "XL", "NGL", "ST", "DARE", "FLOW", "BOOM", "RACE", "BOX", "SHOP", "COKE", "AHH", "GUT", "APPS", "MASS", "RING", "WASH", "SUM", "ICE", "SUN", "LIT", "OFC", "GF", "DIG", "TREE", "GOAT", "MET", "HOOK", "LOOP", "SALT", "SI", "CENT", "DTE", "SAM", "CAT", "FOLD", "ROOF", "COLD", "GL", "PS", "USA", "OI", "RE", "LEG", "HACK", "CCS", "CO", "TBF", "ALEX", "DUST", "OPT", "POOL", "LEE", "MAC", "IP", "TOPS", "LAD", "EAR", "CORE", "UI", "BAND", "RODE", "ET", "GOLF", "EARS", "BOND", "WIRE", "IRL", "FARM", "PACK", "FRI", "SNOW", "NOV", "CPA", "CFA", "ECHO", "CURE", "VICE", "HERD", "GOVT", "COM", "ACC", "SE", "BOB", "AI", "ALT", "NYC", "DUG", "AIM", "PILL", 
"PROS",
"WAT",
"BOB",
"NAIL",
"OFC",
"AGE",
"ONTO",
"CRY",
"HEAR",
]
                    
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
"PELEOTON": "PTON",
"FORD": "F",
"DRAFT KINGS": "DKNG"
    }

    # Holds all of the tickers
TICKERS = open("symbols.txt").read().splitlines()