import config
import requests

def getQuote(ticker):
    apikey = config.alpha_vantage_api
    url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" +  ticker +  "&apikey=" +  apikey
    print(url)
    response = requests.get(url)
    try:
        data = responses[some_key][some_index][...][...]
    except (IndexError, KeyError, TypeError):
        print("EMPTY")
    print(response.status_code)
