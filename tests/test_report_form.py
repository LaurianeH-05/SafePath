import unittest
from app import app
app.secret_key = 'test_secret_key'

class ReportFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_report_form_loads(self):
        response = self.app.get('/report')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Submit a Safety Report", response.data)

    def test_report_submission(self):
        response = self.app.post('/submit_report', data={
            'location': '5th Avenue',
            'type': 'Dark Area',
            'description': 'Poor lighting and suspicious activity'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>Submit a Safety Report</h1>", response.data)
