"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app
from src.counter import COUNTERS

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    def setUp(self):
        self.client = app.test_client()

    """Counter tests"""
    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """Test create and update a counter"""
        client = app.test_client()
        result = client.post('/counters/update')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED) # Check if counter made

        # Save initial counter value
        base = COUNTERS['update']

        # Update counter
        update = client.put('/counters/update')
        self.assertEqual(update.status_code, status.HTTP_200_OK) # Check if counter updated
        self.assertEqual(COUNTERS['update'], base + 1) # Check if counter incremented

    def test_read_a_counter(self):
        """Test read counter"""
        client = app.test_client()
        result = client.post('/counters/read')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED) # Check if counter made

        # Read counter
        read = client.get('/counters/read')
        self.assertEqual(read.status_code, status.HTTP_200_OK) # Check if counter read

        # Read invalid counter
        invalid = client.get('/counters/invalid')
        self.assertEqual(invalid.status_code, status.HTTP_404_NOT_FOUND) # Check if counter not found
