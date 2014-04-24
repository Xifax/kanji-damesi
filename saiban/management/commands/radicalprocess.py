from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from saiban.models import Radical

from optparse import make_option

import requests
from requests import RequestException
from bs4 import BeautifulSoup


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--update',
                    action='store_true',
                    dest='update',
                    default=True,
                    help='Update radicals with info and alternative reading'),
    )
    help = 'Update information on kanji radicals'

    # public spreadsheet with radicals collection (every radical from
    # kradfile)
    url = ('https://docs.google.com/spreadsheet/ccc?'
           'key=0AkI3jF0lqjOLdGZobEV0bHNHRW1MSmF6dnd6TGh6c3c#gid=0')

    def handle(self, *args, **options):
        # Update radical information
        if options['update']:
            results = self.prepare()
            for radical in Radical.objects.all():
                rad = None
                # Try to find by alt
                if radical.front not in results:
                    for item in results:
                        if results[item]['alt'] == radical.front:
                            results[item]['alt'] = item
                            rad = results[item]
                # Or simply use key
                else:
                    rad = results.get(radical.front)

                if rad is not None:
                    radical.name = rad['name']
                    radical.info = rad['primitive']
                    radical.alternative = rad['alt']
                    radical.strokes = rad['strokes']
                    radical.position = rad['position']
                    radical.save()

    def get_radicals_info(self):
        """Get info"""
        try:
            return requests.get(self.url).content
        except RequestException:
            return ''

    def prepare(self):
        """Parse radicals info into dictionary"""
        results = {}

        # Parse resulting table
        info = self.get_radicals_info()
        soup = BeautifulSoup(info, 'lxml')
        rows = soup.find_all('tr')
        # Prepare dictionary entry for each row
        for row in rows:
            cells = row.find_all('td')
            # Total number of columns, including bogus one
            if len(cells) == 7:
                # todo: strip fields from spaces
                radical = cells[1].get_text()
                if radical:
                    results[radical] = {
                        # Alternative radical
                        'alt': self.get_cell(cells, 2),
                        # Number of strokes
                        'strokes': self.get_cell(cells, 3),
                        # Japanese name
                        'name': self.get_cell(cells, 4),
                        # Primitive name (RTK, english)
                        'primitive': self.get_cell(cells, 5),
                        # Radical position
                        'position': self.get_cell(cells, 6)
                    }

        return results

    def get_cell(self, cells, n):
        """Get trimmed cell content"""
        return cells[n].get_text().strip() if cells[n] else ''
