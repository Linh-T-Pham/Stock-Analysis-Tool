
import unittest
from unittest import TestCase
from server import app
from model import connect_to_db, db, User, Company, User_Company, DailyPrice


class FlaskTests(TestCase):
    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def test_homepage(self):
        """Test homepage"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h1>Hello</h1>", result.data)

    def user(self):
        """Test user_stock route"""

        result = self.client.get("/user_stock")
        self.assertEqual(result.status_code,200)
        self.assertIn(b"<h3>Current Market Data</h3>", result.data)

    def test_correlation(self):
        """Test correlation.json route"""

        result = self.client.get('/correlation.json')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h3>Correlation Analysis</h3>', result.data)

    def test_correlation(self):
        """Test sector route"""

        result = self.client.get('/sector')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<title>Sector Performance</title>', result.data)

    def test_correlation(self):
        """Test add_stock route"""

        result = self.client.get('/add_stock')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<label>Enter a ticker', result.data)


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

        # write tests here



if __name__ == "__main__":

    unittest.main()
    init_app()