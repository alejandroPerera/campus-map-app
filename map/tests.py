from django.test import TestCase
from django.urls import reverse

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

            self.assertEqual(results[0].coordinates, [-78.510896, 38.031655], 'Incorrect coordinates stored')
            self.assertEqual(results[0].name, 'Rice Hall', 'Incorrect name stored')

            self.assertEqual(results[4].coordinates, [-79.8028, 41.7776], 'Incorrect coordinates stored')
            self.assertEqual(results[4].name, 'Riceville', 'Incorrect name stored')

    def test_get_search_results(self):
        query = 'rice'
        response = self.client.post(reverse('map:search'), data={'search': query})

        self.assertEqual(response.status_code, 200, "Response code is not 200")


class SearchTests(TestCase):

    def setUp(self) -> None:
        print('Creating test database objects')
        ClassModel.objects.create(
            class_number=15927,  # This is the 5 digit unique class ID. Ex: 15927
            class_mnemonic='CS',
            course_number=3240,  # This is the 4 digit course number, but is not specific to section Ex: 3240
            class_section=1,
            class_type='test',
            class_units=0.0,
            class_instructor='test',
            class_days='test',
            class_room='test',
            class_title='test',
            class_topic='test',
            class_status='test',
            class_enrollment=0,
            class_enrollment_limit=0,
            class_waitlist=0,
            # class_combined_with=ClassModel(None),
            class_description='test',
        )

    def test_parse_classes(self):
        search_term = '15927 CS 3240 001'
        query = parse_classes(search_term)

        self.assertEqual(query[0], '15927')
        self.assertEqual(query[1], 'CS')
        self.assertEqual(query[2], '3240')
        self.assertEqual(query[3], '001')

    def test_parse_classes_only_class_number(self):
        search_term = '15927'
        query = parse_classes(search_term)

        self.assertEqual(query[0], '15927')
        self.assertEqual(query[1], None)
        self.assertEqual(query[2], None)
        self.assertEqual(query[3], None)

    def test_parse_classes_only_mnemonic(self):
        search_term = 'CS'
        query = parse_classes(search_term)

        self.assertEqual(query[0], None)
        self.assertEqual(query[1], 'CS')
        self.assertEqual(query[2], None)
        self.assertEqual(query[3], None)

    def test_parse_classes_only_course_number(self):
        search_term = '3240'
        query = parse_classes(search_term)

        self.assertEqual(query[0], None)
        self.assertEqual(query[1], None)
        self.assertEqual(query[2], '3240')
        self.assertEqual(query[3], None)

    def test_parse_classes_only_section_number(self):
        search_term = '001'
        query = parse_classes(search_term)

        self.assertEqual(query[0], None)
        self.assertEqual(query[1], None)
        self.assertEqual(query[2], None)
        self.assertEqual(query[3], '001')

    def test_parse_classes_garbage_in(self):
        search_term = 'ytredghfrdghjuytresxbju'
        query = parse_classes(search_term)

        self.assertEqual(query[0], None)
        self.assertEqual(query[1], None)
        self.assertEqual(query[2], None)
        self.assertEqual(query[3], None)

    def test_parse_classes_building_in(self):
        search_term = 'Thornton Hall'
        query = parse_classes(search_term)

        self.assertEqual(query[0], None)
        self.assertEqual(query[1], None)
        self.assertEqual(query[2], None)
        self.assertEqual(query[3], None)

    def test_parse_classes_4_letter_building(self):
        search_term = 'Rice Hall'
        query = parse_classes(search_term)

        self.assertEqual(query[0], None)
        self.assertEqual(query[1], None)
        self.assertEqual(query[2], None)
        self.assertEqual(query[3], None)
