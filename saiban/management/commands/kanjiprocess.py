from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from saiban.models import Kanji, Radical

import os
from optparse import make_option

# from bs4 import BeautifulSoup
# import requests
from jpnetkit.kradfile import Kradfile

import sqlite3


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--kanji',
                    action='store_true',
                    dest='kanji',
                    default=True,
                    help='Update kanji with data from Kanjidic'
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

    def get(self, row):
        """Parse sqlite query results"""
        return row[0] if row is not None else u''

    def update_kanji(self):
        """Update kanji info from kanjidic"""
        kanjidic = 'data/kanjidic.sqlite'
        if not os.path.isfile(kanjidic):
            raise CommandError('data/kanjidic.sqlite not found')

        # Connect to kanjidic.sqlite
        kanjidic = sqlite3.connect(kanjidic)
        cursor = kanjidic.cursor()
        for kanji in Kanji.objects.filter(processed=False).all():
            xstr = lambda s: 0 if s is None else s
            # Info
            grade, frequency, jlpt = [
                xstr(row) for row in cursor.execute(
                    "SELECT grade, freq, jlpt FROM character "
                    "WHERE literal = '%s'"
                    % kanji.front
                ).fetchone()
            ]

            # Meaning(s)
            glosses = [
                self.get(row) for row in cursor.execute(
                    "SELECT meaning FROM meaning "
                    "WHERE character_literal = '%s' "
                    "AND m_lang='en'"
                    % kanji.front
                ).fetchall()
            ]

            # Reading(s)
            kuns = [
                self.get(row) for row in cursor.execute(
                    "SELECT reading FROM reading "
                    "WHERE character_literal = '%s' "
                    "AND r_type='ja_kun'"
                    % kanji.front
                ).fetchall()
            ]

            ons = [
                self.get(row) for row in cursor.execute(
                    "SELECT reading FROM reading "
                    "WHERE character_literal = '%s' "
                    "AND r_type='ja_on'"
                    % kanji.front
                ).fetchall()
            ]

            nanoris = [
                self.get(row) for row in cursor.execute(
                    "SELECT nanori FROM nanori "
                    "WHERE character_literal = '%s'"
                    % kanji.front
                ).fetchall()
            ]

            # Stroke count
            strokes = self.get(cursor.execute(
                "SELECT stroke_count FROM stroke_count "
                "WHERE character_literal = '%s'"
                % kanji.front
            ).fetchone())

            # Update kanji
            kanji.on = u', '.join(ons)
            kanji.kun = u', '.join(kuns)
            kanji.nanori = u', '.join(nanoris)
            kanji.gloss = u', '.join(glosses)

            kanji.jlpt = jlpt
            kanji.grade = grade
            kanji.strokes = strokes
            kanji.frequency = frequency

            kanji.save()

            # log result to console
            self.stdout.write(
                '%s: %s | %s; %s; %s; [%d-%d-%d-%d]' % (
                    kanji.front,
                    ', '.join(glosses),
                    ', '.join(kuns),
                    ', '.join(ons),
                    ', '.join(nanoris),
                    strokes, grade, frequency, jlpt
                )
            )

        kanjidic.close()

    def update_radicals(self):
        """Create radical decomposition for each kanji"""
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

    def handle(self, *args, **options):
        # Process kanji info using kanjidic
        if options['kanji']:
            self.update_kanji()

        # TODO: tatoeba for examples

        # Use kradfile to associate kanji with radicals
        if options['radicals']:
            self.update_radicals()
