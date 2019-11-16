from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, User_Company, Company, DailyPrice
import datetime 
import pandas as pd
# import pandas_datareader.data as web
from api import get_ticker_data


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined

# FOR LOADING NEW COMPANIES
# ticker = request.args.get('ticker')
# name = request.args.get('name')
# company = {ticker: name}
# load_company(company)


@app.route('/charts')
def index():
    

    return render_template("charts.html")


@app.route('/chart.json')
def get_chart():
   
    ticker = request.args.get('comp')
 

    tickers = DailyPrice.query.filter_by(ticker=ticker).all()
  

    dates = []
    close_prices = []
    for t in tickers: 
        dates.append(t.date.month)
        close_prices.append(t.close_p)

    dates.reverse()
    close_prices.reverse()

    data_dict = {
        "dates": dates,
        "close_prices": close_prices
    }
  
    return jsonify(data_dict)
 
@app.route('/variation.json')
def daily_price_variation():

    ticker = request.args.get('comp')

    tickers = DailyPrice.query.filter_by(ticker=ticker).all()

    """Return daily price variation in percentage"""
    dates = []
    per_daily_price_list = []

    for t in tickers:
        per = round(((float(t.open_p - t.close_p)/abs(t.open_p))*100),2)
        per_daily_price_list.append(per)
        dates.append(t.date.month)

    dates.reverse()
    per_daily_price_list.reverse()
      

    data_dict = {

        "labels": dates,
        "datasets": [
            {
                "label": "Daily Price Variation in Percentage",
                "barPercentage": 0.5,
                "barThickness" :2,
                "maxBarThickness": 3,
                "minBarLength":1,
                "backgroundColor": 'rgb(144,238,144)',
                "borderColor": 'rgb(144,238,144)',
                "data":per_daily_price_list
               }
        ]
    }

    return jsonify(data_dict)


@app.route('/login', methods=['GET'])
def login_form():
    """login form."""

    return render_template("login_form.html")


@app.route('/register', methods=['GET'])
def register_form():
    """login form."""

    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_create():
    """Users need to login"""

    email = request.form["email"]
    fname = request.form["firstname"]
    lname = request.form["lastname"]
    password = request.form["password"]

    new_user = User(email=email, fname=fname, lname=lname, password=password)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/login")


@app.route('/login', methods=['POST'])
def login_process():
    """Create login process"""

    email = request.form['email']
    password = request.form['password']
  
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such users")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/charts")


@app.route("/logout")
def logout():
    del session["user_id"]
    flash("Logged Out.")
    return redirect("/charts")


# FOR LOADING NEW COMPANIES
# ticker = request.args.get('ticker')
# name = request.args.get('name')
# company = {ticker: name}
# load_company(company)
@app.route('/add_portfolio', methods=['POST'])
def add_to_profolio():
    """Users enter a ticker on the chart page and add it to their portfolio"""
    
    ticker = request.form["ticker"]

    user_id = session.get('user_id')

    if not user_id:
        return redirect("/login")

    new_ticker = User_Company(ticker=ticker, user_id=user_id)


    db.session.add(new_ticker)
    db.session.commit()

    user = User.query.get(user_id)

    return render_template("myportfolio.html", companies=user.companies)


# @app.route('/calculator', methods=['POST'])
# def create_calculator():

#     """Calculate the total gain and loss and pass them to myprofolio.htm"""  
#     shares = request.form["shares"]
#     total_buy_price = shares * buy_price 

#     total_sell_price = shares * total_sell_price

#     if total_buy_price > total_sell_price:
#         profit = total_sell_price - total_buy_price
#         # return profit 
#     else:
#         loss = total_buy_price - total_sell_price
#         # return loss 

#     return render_template("myportfolio.html",
#                             total_buy_price = total_buy_price,
#                             total_sell_price = total_sell_price,
#                             profit=profit,
#                             loss=loss)

@app.route('/correlation')
def analyze_corr():
    
    ticker1 = request.agrs.get["ticker1"]
    ticker2 = request.agrs.get["ticker2"]


    data_by_ticker = request_api(ticker1, 2019-10-15)
    # print(data_by_ticker)

    for date, value in data_by_ticker.items():
        date = date1
        close_price1 = value["4. close"]
      
    data_by_ticker = request_api(ticker2, 2019-10-15)

    for date, value in data_by_ticker.items():
        date = date2
        close_price2 = value["4. close"]

    dfcomp = web.DataReader(close_price1, close_price2)

    print(dfcomp)
 


if __name__ == "__main__":

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")