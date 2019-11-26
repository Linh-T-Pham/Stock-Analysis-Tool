from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, User_Company, Company, DailyPrice
import datetime as dt
import json
import pandas_datareader.data as pan
import datetime 
import requests


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined

@app.route('/about')
def get_company_info():

    ticker = request.args.get('ticker')

    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker + "/company/quote?token=pk_ab6548b1284345368ccec6e806e70415")
    ticker_api = api_request.json()

    return render_template("homepage.html", ticker=ticker, ticker_api = ticker_api)

#       .--.             .---.
#         /:.  '.         .' ..  '._.---.
#        /:::-.  \.-"""-;` .-:::.     .::\
#       /::'|  `\/  _ _  \'   `\:'   ::::|
#   __.'    |   /  (o|o)  \     `'.   ':/
#  /    .:. /   |   ___   |        '---'
# |    ::::'   /:  (._.) .:\
# \    .='    |:'        :::|
#  `""`       \     .-.   ':/
#        jgs   '---`|I|`---'
#                   '-'


@app.route('/')
def index():
    

    return render_template("charts.html")


#       .--.             .---.
#         /:.  '.         .' ..  '._.---.
#        /:::-.  \.-"""-;` .-:::.     .::\
#       /::'|  `\/  _ _  \'   `\:'   ::::|
#   __.'    |   /  (o|o)  \     `'.   ':/
#  /    .:. /   |   ___   |        '---'
# |    ::::'   /:  (._.) .:\
# \    .='    |:'        :::|
#  `""`       \     .-.   ':/
#        jgs   '---`|I|`---'
#                   '-'

@app.route('/chart.json')
def get_chart():
   
    ticker = request.args.get('comp')
 

    tickers = DailyPrice.query.filter_by(ticker=ticker).all()
  

    dates = []
    close_prices = []
    for t in tickers: 
        dates.append(t.date)
        close_prices.append(t.close_p)

    dates.reverse()
    close_prices.reverse()

    data_dict = {
        "dates": dates,
        "close_prices": close_prices
    }
  
    return jsonify(data_dict)


#       .--.             .---.
#         /:.  '.         .' ..  '._.---.
#        /:::-.  \.-"""-;` .-:::.     .::\
#       /::'|  `\/  _ _  \'   `\:'   ::::|
#   __.'    |   /  (o|o)  \     `'.   ':/
#  /    .:. /   |   ___   |        '---'
# |    ::::'   /:  (._.) .:\
# \    .='    |:'        :::|
#  `""`       \     .-.   ':/
#        jgs   '---`|I|`---'
                  # '-'
 
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
        dates.append(t.date)
      

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

#       .--.             .---.
#         /:.  '.         .' ..  '._.---.
#        /:::-.  \.-"""-;` .-:::.     .::\
#       /::'|  `\/  _ _  \'   `\:'   ::::|
#   __.'    |   /  (o|o)  \     `'.   ':/
#  /    .:. /   |   ___   |        '---'
# |    ::::'   /:  (._.) .:\
# \    .='    |:'        :::|
#  `""`       \     .-.   ':/
#        jgs   '---`|I|`---'
#                   '-'

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

@app.route("/user_portfolio")
def go_to_portfolio():

    return redirect("/user_stock")



@app.route("/correlation.json")
def analyze_corr():
    """Correlate two companies"""
   
    ticker1 = request.args.get("ticker1")
    
    ticker2 = request.args.get("ticker2")

    #set the time frame to fetch stock data
    
    start = dt.datetime(2019, 10, 15)
    end = dt.datetime(2019, 11, 15)

    df1 = pan.DataReader(ticker1, 'av-daily', start, end, 
        api_key="pk_ab6548b1284345368ccec6e806e70415")['close']

    df2 = pan.DataReader(ticker2, 'av-daily', start, end, 
        api_key="pk_ab6548b1284345368ccec6e806e70415")['close']

    per_ticker1 = df1.pct_change()
    per_ticker2 = df2.pct_change()

    datasets = []

    ticker1_dict = per_ticker1.to_dict()
    
    dataset1 = {"label":ticker1, 
                "borderColor": "blue",
                "showLine":False,
                "pointRadius": 7,
                "data": []}
   
    for d1, per1 in ticker1_dict.items():
        if d1 != "2019-10-15":
            dataset1["data"].append({"x":d1, "y":per1})
    
    datasets.append(dataset1)

    

    ticker2_dict = per_ticker2.to_dict()
    dataset2 = {
                "label": ticker2,
                "borderColor": "green",
                "showLine":False,
                "pointRadius": 7,
                "data": []
                }
    
    for d2, per2 in ticker2_dict.items():
        if d2 != "2019-10-15":
            dataset2["data"].append({"x":d2, "y":per2})

    datasets.append(dataset2)


    # for i, price in enumerate(per_ticker1.to_list()):
    #     print(price, type(price))
    #     if i == 0: 
    #         print("\n\n\n\n\n\n")
    #         continue
    #     data.append({"x": price, "y": ticker2_list[i]})

    # print(data)


    data_dict = {
        "datasets": datasets
    }
    print(data_dict)
    
    return jsonify(data_dict)



@app.route("/risk_return_analysis.json")
def create_risk_return():

    """Pull all tickers for that user"""
    user = User.query.get(session['user_id'])
    tickers = user.companies
    
    start = dt.datetime(2018, 10, 15)
    end = dt.datetime(2019, 11, 22)
    
    reTurn_list = []
    risk_list =[]
    data_list = []
    ticker_list = []

    for each_ticker in tickers:
        df = pan.DataReader(each_ticker.ticker, 'av-daily', start, end, 
        api_key="pk_ab6548b1284345368ccec6e806e70415")['close']


        per_ticker = df.pct_change()
        
        reTurn = round(per_ticker.mean(),5)
        reTurn_list.append(reTurn)

        max_ReTurn= max(reTurn_list)
        
        risk = round(per_ticker.std(),5)
        risk_list.append(risk)

        max_risk= max(risk_list)

        data_list.append({"x":reTurn, "y":risk})      
        ticker_list.append(each_ticker.ticker)


    data_dict = {

        "datasets": [{
            "label": "Hi",
            "showLine":False,
            "borderColor": "blue",
            "pointRadius": 7,
            "data": data_list
        }]

    }
    
    return jsonify(data_dict)

@app.route("/risk_return_table")
def create_r_table():
    user = User.query.get(session['user_id'])
    tickers = user.companies
    
    start = dt.datetime(2018, 10, 15)
    end = dt.datetime(2019, 11, 22)
    
    reTurn_list = []
    risk_list =[]
    ticker_list = []

    new_dict1 = {}
    new_dict2 = {}

    for each_ticker in tickers:
        df = pan.DataReader(each_ticker.ticker, 'av-daily', start, end, 
        api_key="pk_ab6548b1284345368ccec6e806e70415")['close']


        per_ticker = df.pct_change()
        
        reTurn = round(per_ticker.mean(),5)
        reTurn_list.append(reTurn)

        max_ReTurn= max(reTurn_list)
        
        risk = round(per_ticker.std(),5)
        risk_list.append(risk)

        max_risk= max(risk_list)    
        ticker_list.append(each_ticker.ticker)

        new_dict1 = dict(zip(ticker_list, risk_list))
        new_dict2 = dict(zip(ticker_list, reTurn_list))

    return render_template("myportfolio.html", 
                           risk_list=risk_list, reTurn_list=reTurn_list)




if __name__ == "__main__":

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")