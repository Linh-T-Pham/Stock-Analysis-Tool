import requests 
import json


def home_request_api():


    api_1 = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BAsub&outputsize=full&apikey=HPTIEFWDT4660PXF")

    print(api_1.json())
    return api_1.json()


    # api_2 = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=HPTIEFWDT4660PXF")

    # print(api_2.json())
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

