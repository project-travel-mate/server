from django.test import TestCase
from api.modules.city.model import City


class TestCity(TestCase):
    def setUp(self):
        random_city_name = "random_city_name"
        random_city_id = 37

        City.objects.create(city_name=random_city_name, id=random_city_id)

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        # lion = Animal.objects.get(name="lion")
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')
        cit
