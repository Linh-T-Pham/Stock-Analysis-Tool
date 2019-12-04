
import unittest
from unittest import TestCase
from server import app
from model import connect_to_db, db, User, Company, User_Company, DailyPrice, init_app, example_data


class FlaskTests(TestCase):
    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def test_homepage(self):
        """Test homepage"""
        print(1)
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Ideas? Issues? Concerns?", result.data)

    def user(self):
        """Test user_stock route"""
        print(2)
        result = self.client.get("/user_stock")
        self.assertEqual(result.status_code,200)
        self.assertIn(b"<h3>Current Market Data</h3>", result.data)


    def add_stock(self):
        """Test add_stock route"""
        print(3)
        result = self.client.get('/add_stock')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'ENTER A TICKER', result.data)


    def sector_performance(self):
        """Test add_stock route"""
        print(4)
        result = self.client.get('/sector')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<title>Sector Performance</title>', result.data)

    def ticker_lookup(self):
        """Test add_stock route"""
        print(5)
        result = self.client.get('/ticker_lookup')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Ticker Lookup</h1>', result.data)

    def test_login(self):
        """Test login page"""
        print(6)
        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Login</h1>', result.data)

    def test_signup(self):
        """Test register page intiall rendering"""
        print(7)
        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<label>First Name:', result.data)


class FlaskTestsDatabase(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        connect_to_db(app, db_uri='postgresql:///testdb')

        db.create_all()
        #currenty example_data doesn't exist
        example_data() #write function in model.py that creates test data for each table

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_database(self):
        """Test that the test db is being used"""
        print(8)
        user_count = len(User.query.all())
        user_company_count = len(User_Company.query.all())
        company_count = len(Company.query.all())

        self.assertEqual(user_count, 3)
        self.assertEqual(user_company_count, 2)
        self.assertEqual(company_count, 2)


if __name__ == "__main__":

    unittest.main()
    # init_app()
