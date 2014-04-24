from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from saiban.models import Kanji, Radical

from optparse import make_option

# from bs4 import BeautifulSoup
# import requests
from jpnetkit.kradfile import Kradfile


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--kanji',
                    action='store_true',
                    dest='kanji',
                    default=True,
                    help='Update kanji with dictionary data '
                    '(readings, translations)'),
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

    help = 'Process existing kanji by populating readings, translations, '
    'examples, etc.'

    def handle(self, *args, **options):
        # TODO: should probably use edict for kanji
        # TODO: tatoeba for examples

        # Use kradfile to associate kanji with radicals
        if options['radicals']:
            krad = Kradfile()
            krad.prepare_radikals()

            # Try to get radicals for each of the available kanji
            for kanji in Kanji.objects.filter(processed=False).all():
                radicals = krad.get_radikals_for(kanji.front)

                # Found radicals for kanji
                if radicals:
                    self.stdout.write(
                        'Found %d radical(s) for kanji %s' % (
                            len(radicals),
                            kanji.front
                        )
                    )

                    for rad in radicals:
                        # If such radical already exists
                        try:
                            radical = Radical.objects.get(front=rad)
                        # Or it's new radical
                        except Radical.DoesNotExist:
                            radical = Radical()
                            radical.front = rad
                            radical.save()

                        # Associate radical with kanji
                        kanji.radicals.add(radical)

                else:
                    self.stdout.write(
                        '-> Could not find radical(s) for kanji %s' %
                        kanji.front
                    )
