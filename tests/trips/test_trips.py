from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase

from api.modules.city.model import City
from api.modules.trips.model import Trip


class TestTripViews(APITestCase):
    """
        Test for remove-user-from-trip API
    """
    api_url_name = "remove-user-from-trip"

    @classmethod
    def setUpTestData(cls):
        """
            run only once for all test methods
            create user and related data objects
        """
        cls.current_user = User.objects.create_user(
            "test_user1",
            "user1@test.com",
            "Django@123")
        cls.friend_user = User.objects.create_user(
            "test_user2",
            "user2@test.com",
            "Django@123")

        cls.city = City.objects.create(
            city_name="test_city",
            latitude=12.34,
            longitude=12.34,)

    def setUp(self):
        """
            run for each test method
            create a new trip
            sign in current-user
        """
        self.trip = Trip.objects.create(
            trip_name="test_trip",
            city=self.city,)
        self.client.force_authenticate(user=self.current_user)

    def test_remove_user_from_trip_invalid_trip(self):
        """
            trip id does not exist
        """
        non_exist_trip_id_url = reverse(self.api_url_name, kwargs={'trip_id': 999, })
        response = self.client.get(non_exist_trip_id_url)
        self.assertEqual(404, response.status_code)

    def test_remove_user_from_trip_unauthorized_user(self):
        """
            current user not associated with trip
        """
        self.url = reverse(self.api_url_name, kwargs={'trip_id': self.trip.id, })
        self.trip.users.add(self.friend_user)
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_remove_user_from_trip_remove_user_success(self):
        """
            trip having multiple user from which current user is removed
        """
        self.url = reverse(self.api_url_name, kwargs={'trip_id': self.trip.id, })
        self.trip.users.add(self.friend_user)
        self.trip.users.add(self.current_user)
        response = self.client.get(self.url)

        flag = self.current_user in self.trip.users.all()
        self.assertFalse(flag)

        trips_count = Trip.objects.all().count()
        self.assertEqual(1, trips_count)

        self.assertEqual(200, response.status_code)

    def test_remove_user_from_trip_delete_trip_success(self):
        """
            trip from which last user is removed and trip is deleted
        """
        self.url = reverse(self.api_url_name, kwargs={'trip_id': self.trip.id, })
        self.trip.users.add(self.current_user)
        response = self.client.get(self.url)

        trips_count = Trip.objects.all().count()
        self.assertEqual(0, trips_count)

        self.assertEqual(200, response.status_code)
