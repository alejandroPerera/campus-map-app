from django.test import TestCase
from .views import *
import json


# Create your tests here.

class SISTest(TestCase):

    def test_ready_overrode(self):
        self.assertTrue(True, "Tests are not running")


class GeoCodeTests(TestCase):

    def test_get_geo_codes(self):
        with open(file='map/static/map/test_geocoding.json') as json_file:
            results = GeoCode.get_geo_codes(json.load(json_file))

            self.assertEqual(results[0].query, 'rice', 'Incorrect query stored')
            self.assertEqual(results[4].query, 'rice', 'Incorrect query stored')

            self.assertEqual(results[0].coordinates, (-78.510896, 38.031655), 'Incorrect coordinates stored')
            self.assertEqual(results[0].name, 'Rice Hall', 'Incorrect name stored')

            self.assertEqual(results[4].coordinates, (-79.8028, 41.7776), 'Incorrect coordinates stored')
            self.assertEqual(results[4].name, 'Riceville', 'Incorrect name stored')

    def test_get_search_results(self):
        query = 'rice'
        response = self.client.post(reverse('map:search'), data={'search': query})
        print(response)

        self.assertEqual(response.status_code, 200, "Response code is not 200")
