from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, User_Company, Company, DailyPrice
import datetime as dt
import json
import pandas_datareader.data as web
import datetime 
import requests


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined


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
        dates.append(t.date.year)
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
      

    data_dict = {

        "labels": dates,
        "datasets": [
            {
                # "label": false,
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


@app.route("/login", methods=["GET"])
def login_form():
    """login form."""

    return render_template("login_form.html")


@app.route("/register", methods=["GET"])
def register_form():
    """login form."""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
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


@app.route("/login", methods=["POST"])
def login_process():
    """Create login process"""

    email = request.form["email"]
    password = request.form["password"]
  
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


@app.route("/add_portfolio", methods=['POST'])
def add_to_profolio():
    """Users enter a ticker on the chart page and add it to their portfolio"""
    
    ticker = request.form["ticker"]

    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    new_ticker = User_Company(ticker=ticker, user_id=user_id)


    db.session.add(new_ticker)
    db.session.commit()

    user = User.query.get(user_id)

    # return render_template("myportfolio.html", companies=user.companies)
    return redirect("/user_stock")



@app.route("/correlation")
def analyze_corr():
    
    ticker1 = request.args.get("ticker1")
    
    ticker2 = request.args.get("ticker2")

    #set the time frame to fetch stock data
    
    start = dt.datetime(2019, 5, 15)
    end = dt.datetime(2019, 11, 15)

    df1 = web.DataReader(ticker1, 'av-daily', start, end, api_key= "pk_ab6548b1284345368ccec6e806e70415")['close']

    df2 = web.DataReader(ticker2, 'av-daily', start, end, api_key= "pk_ab6548b1284345368ccec6e806e70415")['close']

    x1 = df1.pct_change()
    print(x1)
    
    y1 = df2.pct_change()
    print(x2)

    data_dict = {

        "datasets": [
            {
                "label": "Scatter Dataset",
                "backgroundColor": 'rgb(144,238,144)',
                "borderColor": 'rgb(144,238,144)',
                "data":[{
                      x: x1,
                      y: y1

                }]
               }
        ]
    }

    # return jsonify(data_dict)
    return render_template("myportfolio.html")

@app.route("/user_stock")
def add_stock():

    user = User.query.get(session['user_id'])
    tickers = user.companies

    response_list = []

    for each_ticker in tickers:

        api = requests.get("https://cloud.iexapis.com/stable/stock/"+ each_ticker.ticker +"/quote?token=pk_ab6548b1284345368ccec6e806e70415")   
        ticker_api = api.json()
        response_list.append(ticker_api)



    return render_template("myportfolio.html",
                            ticker_data=response_list)





if __name__ == "__main__":

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")