from unittest import TestCase
from server import app
from model import connect_to_db, db, User, Company, User_Company, DailyPrice
# from flask import session 



class FlaskTests(TestCase):
    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<label>Enter a ticker", result.data)

    def test_userstock(self):

        result = self.client.get("/user_stock")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h3>Current Market Data</h3>', result.data)

# class FlaskTestsDatabase(TestCase):
#     def setUp(self):
#         self.client = app.test_client()
#         app.config['TESTING'] = True
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#         connect_to_db(app, db_uri='postgresql:///testdb')

#         db.create_all()
#         #currenty example_data doesn't exist
#         example_data() #write function in model.py that creates test data for each table

#         def tearDown(self):
#             db.session.close()
#             db.drop_all()

#         #write tests here



if __name__ == "__main__":
    import unittest

    unittest.main()