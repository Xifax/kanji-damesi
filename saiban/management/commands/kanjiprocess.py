from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from saiban.models import Kanji, Compound, Radical, KanjiGroup

from optparse import make_option
import json

from bs4 import BeautifulSoup
import requests

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--kanji',
            action='store_true',
            dest='kanji',
            default=True,
            help='Update kanji with dictionary data (readings, translations)'),
        make_option('--compounds',
            action='store_true',
            dest='compounds',
            default=False,
            help='Find usage examples for the kanji'),
        make_option('--radicals',
            action='store_true',
            dest='radicals',
            default=False,
            help='Find radical decomposition for each kanji'),
        make_option('--examples',
            action='store_true',
            dest='examples',
            default=False,
            help='Find examples for compounds'),
    )

    help = 'Process existing kanji by populating readings, translations, examples, etc.'

    def handle(self, *args, **options):
        # TODO: should probably use edict for kanji
        # TODO: tatoeba for examples
        # TODO: kradfile for radicals
        pass
