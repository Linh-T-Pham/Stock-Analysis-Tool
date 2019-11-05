from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import correlation
# from collections import defaultdict

db = SQLALchemy()

class User(db.Model):
"""User adds favorite stocks to their profolios"""

    __tablename__ = 'users'

    user_id = db.Column(db.Interger, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(20), nullable = True)
    lname = db.Column(db.String(20), nullable = True)
    email = db.Column(db.String(30), nullable = True)

    def __repr__(self):
        """Provide user's information in a helpful format"""
        return f"<User {user_id=self.user_id} {first_name=self.fname} {last_name=self.lname}>"

class Company(db.Model):
    """Create companies table"""

    __tablename__ = 'companies'


    ticker = db.Column(db.String(10), primary_key = True, unique=True)
    name = db.Column(db.String(10), nullable=False)

    def_repr_(self):

        return f"<Company ticker={self.ticker} company_name={self.name}>"
    

class User_Company(db.Model):
    """Create user_comapny tables to establish relationship"""

    __tablename__ = 'user_companies'

    main_id = db.Column(db.Interger, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Interger, db.ForeignKey('users.user_id'), index=True)
    ticker = db.Column(db.String(10),db.ForeignKey('companies.ticker'), index=True)

    #Define the relationship to User

    user = db.relationship('User', backref = "user_companies")

    company = db.relationship('Company', backref = "user_companies")


    def_repr_(self):

    return f"<User_Company main_id={self.main_id} user_id={self.user_id} ticker={self.ticker}>"

class Daily_Price(db.Model):
    """Create prices tables """

    __tablename__ = 'prices'

    price_id = db.Column(db.Interger, autoincrement=True, primary_key=True)
    ticker = db.Column(db.String(10), db.ForeignKey('companies.ticker'), unique=True)
    date = db.Column(db.DateTime)
    open_p = db.Column(db.Interger, nullable = True)
    high_p = db.Column(db.Interger, nullable = True)
    low_p = db.Column(db.Interger, nullable = True)
    close_p = db.Column(db.Interger, nullable = True)
    volume_p = db.Column(db.Interger, nullable = True)

    company = db.relationship('Company', backref = "prices")

    def_repr_(self): 

    return f"<Daily_Price close_p={self.close_p} volume_p={self.volume_p}>"


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print("Connected to DB.")