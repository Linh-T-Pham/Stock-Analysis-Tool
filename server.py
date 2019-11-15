from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, sessions, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, User_Company, Company, DailyPrice
import datetime 


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


@app.route('/login', methods=['POST'])
def login_create():
    """Users need to login"""

    email = request.form["email"]
    fname = request.form["firstname"]
    lname = request.form["lastname"]
    password = request.form["password"]

    new_user = User(email=email, fname=fname, lname=lname, password=password)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/charts")

@app.route('/login', methods=['POST'])
def login_process():

    email = request.form['email']
    password = request.form['password']
    # fname = request.form['firstname']
    # lname = request.form['lastname']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such users")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/")

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
@app.route('/add_profolio', methods=['POST'])
def add_to_profolio():

    ticker = request.form["ticker"]

    new_ticker = User_Company(ticker=ticker)

    db.session.add(new_ticker)
    db.session.commit()

    return render_template("myprofolio.html")


@app.route('/calculator')
def create_calculator():


    total_buy_price = shares * buy_price 

    total_sell_price = shares * total_sell_price

    if total_buy_price > total_sell_price:
        profit = total_sell_price - total_buy_price
        return profit 
    else:
        loss = total_buy_price - total_sell_price
        return loss 



   


if __name__ == "__main__":

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")