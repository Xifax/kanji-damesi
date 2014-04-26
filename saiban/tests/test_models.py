# coding: utf-8
from django.test import TestCase

# Create your tests here.

from saiban.models import (
    Kanji,
    # Radical,
    # Compound,
    # KanjiGroup
)


class ModelTests(TestCase):

    def test_may_get_kanji_as_json(self):
        """
        Should return dictionary with object data
        """
        kanji_data = {
            'front': u'漢',
            'on': u'myo',
            'kun': u'hyo',
            'gloss': 'pyo',
        }
        kanji = Kanji(**kanji_data)
        kanji.save()
        json = kanji.as_json()
        for key in kanji_data:
            self.assertIn(key, json)
