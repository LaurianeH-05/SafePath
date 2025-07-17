import unittest
from app import app

class RoutePageTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_route_page_get(self):
        response = self.app.get('/route')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Start Location", response.data)