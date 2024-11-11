import unittest
import sys
sys.path.append(r'C:\Users\Zeus\Documents\GitHub\Flask_NetTowers')

from app import app

class TestRegistration(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"]= True
        app.config["DEBUG"] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = '/reg'

    def test_missing_phone_number(self):
        response = self.app.post('/reg', data={
            "delivery_address": "123 Main St",
            "recipient_name": "John Doe"
            # ,"phone": "324234"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Phone number is required', response.data)

    def test_missing_delivery_address(self):
        response = self.app.post('/reg', json={
            "phone_number": "1234567890",
            "recipient_name": "John Doe"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Delivery address is required', response.data)

    def test_missing_recipient_name(self):
        response = self.app.post('/reg', json={
            "phone_number": "1234567890",
            "delivery_address": "123 Main St"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Recipient name is required', response.data)

    def test_successful_registration(self):
        response = self.app.post(self.base_url, data={
            "phone": "1234567890",
            "address": "123 Main St",
            "name": "John Doe"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration', response.data)
        self.assertIn(b'1234567890', response.data)

    def test_phone_length(self):
        response = self.app.post(self.base_url, data={
            "phone": "12345",
            "address": "123 Main St",
            "name": "John Doe"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'its lower than 7 and 10', response.data)
