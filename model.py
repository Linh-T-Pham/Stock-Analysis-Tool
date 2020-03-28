from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()

class User(db.Model):
    """User adds favorite stocks to their profolios"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(30), nullable=True, unique = True)
    password = db.Column(db.String(100), nullable=True)


    companies = db.relationship("Company",
                                backref="users",
                                secondary="user_companies")

    def __repr__(self):
        """Provide user's information in a helpful format"""

        return f"<User user_id={self.user_id} first_name={self.fname} last_name={self.lname}>"

class Company(db.Model):
    """Create companies table"""

    __tablename__ = "companies"

    ticker = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):

        return f"<Company ticker={self.ticker} company_name={self.name}>"

class User_Company(db.Model):
    """Create user_comapny tables to establish relationship"""

    __tablename__ = "user_companies"

    user_comp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    ticker = db.Column(db.String(10),db.ForeignKey("companies.ticker"))
  

    def __repr__(self):

        return f"<User_Company main_id={self.main_id} user_id={self.user_id} ticker={self.ticker}>"


class DailyPrice(db.Model):
    """Create prices tables """

    __tablename__ = "daily_prices"

    price_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ticker = db.Column(db.String(4),
                       db.ForeignKey("companies.ticker"))
    date = db.Column(db.DateTime)
    open_p = db.Column(db.Float, nullable=True)
    high_p = db.Column(db.Float, nullable=True)
    low_p = db.Column(db.Float, nullable=True)
    close_p = db.Column(db.Float, nullable=True)
    volume_p = db.Column(db.Float, nullable=True)

    company = db.relationship("Company", backref="daily_prices")

    def __repr__(self): 

        return f"<Daily_Price close_p={self.close_p} volume_p={self.volume_p}>"


##############################################################################
# Helper functions

def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app, "postgresql:///testdb")
    print("Connected to DB.")

def example_data():
    """Populate a database with sample data for testing purposes."""
    db.create_all()

    User.query.delete()
    User_Company.query.delete()
    Company.query.delete()

    #sample users
    user1 = User(user_id=1, fname="Nikki", lname="test", email='12@test.com', password="password")
    user2 = User(user_id=2, fname="Nina", lname="test", email='34@test.com', password="password")
    user3 = User(user_id=3, fname="Pauline", lname="test", email='56@test.com', password="password")
    db.session.add_all([user1, user2, user3])
    db.session.commit()
    
    #sample companies
    company1 = Company(ticker="FIT", name="Fitbit")
    company2 = Company(ticker="PINS",name="Pinterest")

    # sample user_companies
    user_company1 = User_Company(user_comp_id=1, user_id=1, ticker="FIT")
    user_company2 = User_Company(user_comp_id=2, user_id=2, ticker="PINS")

    # Add all to sesson and commit
    db.session.add_all([user1, user2 ,user3, company1, company2, user_company1, user_company2])
    db.session.commit()

def connect_to_db(app, db_uri="postgresql:///stocks"):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print("Connected to DB.")











    