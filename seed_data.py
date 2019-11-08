import datetime
from sqlalchemy import func
from model import User, Company, User_Company, DailyPrice, connect_to_db, db
from api import get_ticker_data
from server import app



# def load_users():
  

#     user = User(user_id=user_id,
#                 fname=fname,
#                 lname=lname,
#                 email=email)
    
#     db.session.add(user)
    
#     db.session.commit()


def load_company():

    db.create_all()

    name_dict = { "MSFT":"Microsoft" ,
                "PYPl" : "PayPal",
                "NVDA": "Nvidia",
                "CRM" : "Salesforce", 
                "TWLO": "Twilio",
                "AAPL" : "Apple",
                "SQ" : "Square",
                "BA": "Boeing",
                "SHOP": "Shopify" }
               

    for ticker, name in name_dict.items():
        company = Company(ticker=ticker, name=name)

        db.session.add(company)

        data_by_ticker = request_api(ticker, 2019)

        for date, value in data_by_ticker.items():
            date = date
            open_p = value["1. open"]
            high_p = value["2. high"]
            low_p = value["3. low"]
            close_p = value["4. close"]
            volume_p = value["5. volume"]

    
            daily_price = DailyPrice(date=date,
                                     open_p=open_p,
                                     low_p=low_p,
                                     high_p=high_p,
                                     close_p=close_p,
                                     volume_p=volume_p)
            
            company.daily_prices.append(daily_price)
    
        db.session.commit()

    


# def load_users_company(ticker):
  
#     data_by_ticker = request_api(ticker)
    

#     user_company = User_Company(user_company_id=user_company_id,
#                                 user_id=user_id,
#                                 ticker=ticker)
 

    # db.session.add(user_company)
    
    # db.session.commit()



def load_DailyPrice(ticker):
    """Load daily price by ticker into dailyprice table """

    data_by_ticker = request_api(ticker)
#     # print(data_by_ticker)

# load_DailyPrice('BA')

    """Define columns'values for DailyPrice table"""



# def load_users_company(ticker):
  
#     data_by_ticker = request_api(ticker)
    

#     user_company = User_Company(user_company_id=user_company_id,
#                                 user_id=user_id,
#                                 ticker=ticker)
 

    # db.session.add(user_company)
    
    # db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)










