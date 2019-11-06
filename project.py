import requests 
import json


def home_request_api(symbol):


    api = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=full&apikey=HPTIEFWDT4660PXF".format(symbol))

    company_api = api.json()


    """Get 5 years of daily_price data from 2014-11-01 to present"""

    # for date, value in company_api["Time Series (Daily)"].items():

    #     if date > "2013-12-5":
    #         print(f"{date} : {value}")





def load_DailyPrice():
    """Load stock daily prices from API into databases."""

    """Get 5 years of daily_price data from 2014-11-01 to present"""

    for date, value in company_api["Time Series (Daily)"].items():

        if date > "2013-12-5":
            print(f"{date} : {value}")

            daily_price = Daily_Price(ticker=ticker,
                                     open_p=open_p,
                                     low_p=low_p,
                                     high_p=high_p,
                                     close_p=close_p,
                                     volume=volume)
    

    # List of stocks
    # MSFT : Microsoft 
    # PYPl : PayPal 
    # NVDA : Nvidia 
    # CRM : Salesforce 
    # TWLO: Twilio
    # AAPL : Apple
    # SQ : Square
    # BA : Boeing
    # SHOP: Shopify 
    # SPOT: Spotify
    # OKTA: Okta 

