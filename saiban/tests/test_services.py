# coding: utf-8
from django.test import TestCase

import factory

from saiban.services.quiz import (
    get_random_kanji_group,
    # get_new_random_kanji
)
from saiban.models import (
    Kanji,
    KanjiGroup,
    # Radical,
    # Compound,
)

# Let's test them services


class KanjiGroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = KanjiGroup

    level = 1
    info = u'Test'

    # kanji = factory.RelatedFactory(
    #     'saiban.tests.test_services.KanjiFactory',
    #     'kanji'
    # )

class AnotherKanjiGroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = KanjiGroup

    level = 2
    info = u'Another test'


class KanjiFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Kanji

    front = u'和'
    kun = u'やわ.らぐ'
    on = u'ワ'
    gloss = u'harmony'

    group = factory.SubFactory(KanjiGroupFactory)


class ServiceTests(TestCase):

    def test_may_get_random_kanji_group(self):
        """
        Should return random kanji group from level specified
        """
        kanji = KanjiFactory.create()
        kanjiGroup = KanjiGroupFactory.create()
        anotherKanjiGroup = AnotherKanjiGroupFactory.create()

        level = 1
        random_group = get_random_kanji_group(level)
        self.assertEquals(random_group.level, level)
