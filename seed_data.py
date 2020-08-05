from datetime import datetime
from sqlalchemy import func
from model import User, Company, User_Company, DailyPrice, connect_to_db, db
from api import get_ticker_data
from server import app


def load_company():

    db.create_all()

    name_dict = { 
                    
                # "DIS": "Walt Disney",
                # "NKE": "Nike",
                # "M": "Nike"    

                 }
              
    for ticker, name in name_dict.items():
        company = Company(ticker=ticker, name=name)

        db.session.add(company)

        data_by_ticker = get_ticker_data(ticker)

        for date, value in data_by_ticker.items():
            if date >= "2018-08-30":
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

# NOTE: 
# Udpated the link after storing the data in database. 
# On seed_data.py, change the name dict 
# with old ticker and company name to new ones. 
# Then on the terminal, run seed_data.py and call the fct load_company()

if __name__ == "__main__":
    connect_to_db(app)










