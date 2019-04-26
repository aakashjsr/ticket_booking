from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.messages import get_messages

from seats.models import Seat


class IndexViewTest(TestCase):
    def setUp(self):
        # Clean up run after every test method.
        self.url = reverse("index")
        self.client = Client()

    def test_data_migration(self):
        """
        assert that 30 seats are created as data migration
        """
        self.assertEqual(Seat.objects.count(), 30)

    def test_rendering(self):
        """
        Asserts if correct template is rendered
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        # assert all seats are rendered in ui
        self.assertEqual(len(response.context["seats"]), Seat.objects.all().count())


class BookingViewTest(TestCase):
    def setUp(self):
        self.url = reverse("seats:book")
        self.client = Client()
        self.seat = Seat.objects.get(id=1)

    def test_book_available_seat(self):
        """
        Test booking of an available ticket
        """
        self.assertEqual(self.seat.status, Seat.AVAILABLE)
        response = self.client.post(
            self.url, {"email": "a@a.com", "name": "test user", "seat": 1}, follow=True
        )

        self.seat.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        # Test redirection back to home page
        self.assertTemplateUsed(response, "index.html")
        self.assertEqual(self.seat.status, Seat.BOOKED)
        self.assertEqual(self.seat.booked_by.email, "a@a.com")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Your seat has been successfully booked.")

    def test_multiple_booking_of_same_ticket(self):
        """
        Test that one seat cannot be booked by multiple user
        """
        self.assertEqual(self.seat.status, Seat.AVAILABLE)
        response_1 = self.client.post(
            self.url, {"email": "a@a.com", "name": "test user", "seat": 1}, follow=True
        )
        response_2 = self.client.post(
            self.url, {"email": "b@b.com", "name": "test user", "seat": 1}, follow=True
        )

        self.seat.refresh_from_db()
        self.assertEqual(response_1.status_code, 200)
        # Test redirection back to home page
        self.assertTemplateUsed(response_1, "index.html")
        self.assertEqual(self.seat.status, Seat.BOOKED)
        self.assertEqual(self.seat.booked_by.email, "a@a.com")

        messages_1 = list(get_messages(response_1.wsgi_request))
        messages_2 = list(get_messages(response_2.wsgi_request))
        # response 1 should have no error message
        self.assertEqual(str(messages_1[0]), "Your seat has been successfully booked.")
        # response 2 should have error message
        self.assertEqual(str(messages_2[0]), "This seat is no longer available.")

    def test_single_user_seat_booking(self):
        """
        Test that only one seat can be booked by user
        """
        self.assertEqual(self.seat.status, Seat.AVAILABLE)
        response_1 = self.client.post(
            self.url, {"email": "a@a.com", "name": "test user", "seat": 1}, follow=True
        )
        response_2 = self.client.post(
            self.url, {"email": "a@a.com", "name": "test user", "seat": 2}, follow=True
        )

        self.seat.refresh_from_db()
        self.assertEqual(response_1.status_code, 200)
        # Test redirection back to home page
        self.assertTemplateUsed(response_1, "index.html")
        self.assertEqual(self.seat.status, Seat.BOOKED)
        self.assertEqual(self.seat.booked_by.email, "a@a.com")

        messages_1 = list(get_messages(response_1.wsgi_request))
        messages_2 = list(get_messages(response_2.wsgi_request))
        # response 1 should have no error message
        self.assertEqual(str(messages_1[0]), "Your seat has been successfully booked.")
        # response 2 should have error message
        self.assertEqual(str(messages_2[0]), "You can book only one seat.")
