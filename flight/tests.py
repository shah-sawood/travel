"""alll tests cases of flight application goes here"""
from django.test import Client, TestCase

# Create your tests here.
class FlightTestCase(TestCase):
    """test cases for flight application"""

    def test_index_page(self):
        """tests the status of index page"""
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_flights_page(self):
        """checks whether flights page displays departed flights or not"""
        client = Client()
        response = client.get("/flights/")
        self.assertEqual(response.status_code, 200)
