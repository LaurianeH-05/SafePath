import unittest
from unittest.mock import patch, MagicMock
from crime import get_crime_coordinates, client
from sodapy import Socrata

class TestCrime(unittest.TestCase):
    @patch('crime.client')
    def test_get_crime_coordinates(self, mock_client):
        # Fake API response
        mock_client.get.return_value = [
            {
                'latitude': '39.1',
                'longitude': '-77.1',
                'location': '123 Main St',
                'offence_code': '2303',
                'date': '2024-05-01T12:34:56.000'
            },
            {
                'latitude': '38.9',
                'longitude': '-77.2',
                'location': '456 Elm St',
                'offence_code': '9999',
                'date': '2024-05-02T08:00:00.000'
            }
        ]
        expected = [
            (39.1, -77.1, '123 Main St', '2303', 'Theft from Auto', '2024-05-01 12:34:56'),
            (38.9, -77.2, '456 Elm St', '9999', 'Unknown', '2024-05-02 08:00:00')
        ]
        result = get_crime_coordinates()
        self.assertEqual(result, expected)

    def test_client_instance(self):
        self.assertIsInstance(client, Socrata)
        self.assertEqual(client.domain, "data.montgomerycountymd.gov")

if __name__ == '__main__':
    unittest.main()