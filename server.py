from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, sessions, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, User_Company, Company, DailyPrice




app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined



@app.route('/')
def index():
    

    return render_template("charts.html")


@app.route('/chart.json')
def get_chart():
   
    ticker = request.args.get('comp')
    print("\n\n\n\n", ticker)
    
    tickers = DailyPrice.query.filter_by(ticker=ticker).all()
  

    dates = []
    close_prices = []
    for t in tickers: 
        dates.append(t.date)
        close_prices.append(t.close_p)

    dates.reverse()
    close_prices.reverse()

    data_dict = {
        "labels": dates,
        "datasets": [
            {
                # "label": "Microsoft",
                "fill": True,
                "lineTension": 0.5,
                "backgroundColor": "rgba(151,187,205,0.2)",
                "borderColor": "rgba(151,187,205,1)",
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(151,187,205,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 10,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(151,187,205,1)",
                "pointHoverBorderWidth": 2,
                "pointHitRadius": 5,
                "data": close_prices,
                "spanGaps": False}
        ]
    }
    
    return jsonify(data_dict)
 




# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""

#     return render_template("login_form.html")

# @app.route('/login', methods=['POST'])
# def login_create():
#     """Users need to login"""

#     email = request.form["email"]s
#     fname = request.form["firstname"]
#     lname = request.form["lastname"]

#     if not user:
#         flash("No such user")
#         return redirect("/login")







if __name__ == "__main__":

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")