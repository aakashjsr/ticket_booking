from django.test import TestCase, Client
from django.shortcuts import reverse

from seats.models import Seat


class IndexViewTest(TestCase):

    def setUp(self):
        # Clean up run after every test method.
        self.url = reverse("index")
        self.client = Client()

    def test_data_migration(self):
        # assert that 30 seats are created as data migration
        self.assertEqual(Seat.objects.count(), 30)

    def test_rendering(self):
        response = self.client.get(self.url)
        print(response.status_code)