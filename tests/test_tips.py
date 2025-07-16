import unittest
from app import app

class TestTipsPage(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_tips_page(self):
        response = self.app.get('/tips')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Stick to well-lit main roads", response.data)
