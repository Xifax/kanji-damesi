# encoding: utf-8
#from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from saiban.models import Kanji, Radical, Compound, Example

import os
import random
import csv
from optparse import make_option

from jpnetkit.kradfile import Kradfile
#from jpnetkit.weblio import Weblio
# from jpnetkit.wordnet import Wordnet
# from jpnetkit.mecab import Mecab

from saiban.mecab import MeCab

import sqlite3
from jcconv import kata2hira


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--kanji',
                    action='store_true',
                    dest='kanji',
                    default=False,
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
        make_option('--associate-examples',
                    action='store_true',
                    dest='associate-examples',
                    default=False,
                    help='Associate examples with compounds'),
        make_option('--check-status',
                    action='store_true',
                    dest='check',
                    default=False,
                    help='Check kanji status (processed or not)'),
    )

    help = 'Process existing kanji by populating readings, translations, '
    'examples, etc.'

    def get(self, row):
        """Parse sqlite query results"""
        return row[0] if row is not None else u''

    def check_kanji(self):
        """Check, if kanji may be considered as processed"""

        # Should contain major info fields
        # Should have associated group
        # Should have associated compounds
        # Should have associated radicals

        pass

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

    def update_compounds(self):
        """Create compounds for each of the kanji"""
        jmdict = 'data/jmdict.sqlite'
        if not os.path.isfile(jmdict):
            raise CommandError('data/jmdict.sqlite not found')

        # Connect to jmdict.sqlite
        jmdict = sqlite3.connect(jmdict)
        cursor = jmdict.cursor()

        for kanji in Kanji.objects.filter(processed=False).all():
            if len(kanji.compounds.all()) == 0:
                # Query jmdict with like %front% to get some of the examples

                # Get 50 compound(s) ordered by length (starting with shortest)
                compounds = [c[0] for c in cursor.execute(
                    "SELECT DISTINCT keb FROM k_ele "
                    "WHERE keb like '%" + kanji.front + "%' "
                    "AND LENGTH(keb) > 1 "
                    "ORDER BY LENGTH(keb) ASC "
                    "LIMIT 50 "
                ).fetchall()]

                # Post-process: randomly select 10 of the compounds
                try:
                    compounds = random.sample(compounds, 10)
                except ValueError:
                    pass

                # Get glosses and readings and related stuff

                self.stdout.write(kanji.front)
                for compound in compounds:
                    # Get id
                    id = cursor.execute(
                        "SELECT entry_ent_seq FROM k_ele WHERE keb = '%s'"
                        % compound
                    ).fetchone()

                    # Get sense id(s)
                    senses = [sense[0] for sense in cursor.execute(
                        "SELECT id FROM sense WHERE entry_ent_seq = '%d'"
                        % id[0]
                    ).fetchall()]

                    # Get readings
                    readings = [self.get(row) for row in cursor.execute(
                        "SELECT reb FROM r_ele WHERE entry_ent_seq = '%d'"
                        % id[0]
                    ).fetchall()]
                    if len(readings) > 1:
                        readings = ', '.join(readings)
                    else:
                        readings = readings[0]

                    # Get gloss(es)
                    glosses = []
                    for sense in senses:
                        glosses += [self.get(row) for row in cursor.execute(
                            "SELECT gloss FROM gloss WHERE sense_id = '%d' "
                            "AND lang='eng'"
                            % sense
                        ).fetchall()]

                        # Get pos
                        pos = cursor.execute(
                            "SELECT pos FROM pos WHERE sense_id = '%d'"
                            % sense
                        ).fetchone()
                        if pos:
                            pos = pos[0]

                    glosses = '; '.join(glosses)

                    # Get similar
                    # Get antonyms

                    # Try to create compound or get existing
                    try:
                        compound = Compound.objects.get(front=compound)
                    # It's a new compound!
                    except Compound.DoesNotExist:
                        compound = Compound(
                            front=compound,
                            reading=readings,
                            gloss=glosses,
                            pos=pos
                        )
                        compound.save()

                    # Associate compound with kanji
                    kanji.compounds.add(compound)

                    self.stdout.write(
                        '%s: %s | %s [%s]' %
                        (compound, readings, glosses, pos)
                    )

                self.stdout.write('***')

    def update_examples(self):
        """Find examples for some|each of the compounds"""

        # Tatoeba
        examples = 'data/sentences.csv'
        links = 'data/links.csv'
        if os.path.exists(examples) and os.path.exists(links):

            # Prepare translations
            self.stdout.write('Processing sentence links...')
            relations = {}
            with open(links, 'rb') as tatoeba_links:
                reader = csv.DictReader(
                    tatoeba_links,
                    fieldnames=('id', 'reference'),
                    delimiter=b'\t'
                )
                for row in reader:
                    relations.setdefault(row['id'], []).append(
                        row['reference']
                    )

            self.stdout.write('Sentence links processed.')
            self.stdout.write('Processing JP-ENG sentences...')

            # Prepare examples
            sentences = {}
            translations = {}
            with open(examples, 'rb') as tatoeba_examples:
                reader = csv.DictReader(
                    tatoeba_examples,
                    fieldnames=('id', 'lang', 'sentence'),
                    delimiter=b'\t'
                )
                for row in reader:
                    if row['lang'] == 'jpn':
                        sentences[row['id']] = {
                            'sentence': row['sentence'],
                            'relations': relations.get(row['id'], [])
                        }
                    elif row['lang'] == 'eng':
                        translations[row['id']] = {
                            'sentence': row['sentence'],
                            'relations': relations.get(row['id'], [])
                        }

            self.stdout.write('JP-ENG sentences processed.')
            self.stdout.write('Saving sentences to the DB...')

            # Prepare example, translation and reading
            duplicates = 0
            tagger = MeCab.Tagger()
            for id, example in sentences.iteritems():
                # Examples and translation
                gloss = ''
                front = example['sentence']
                for ref in example['relations']:
                    translation = translations.get(ref, '')
                    if translation:
                        gloss = translation['sentence']

                # Readings
                readings = []

                node = tagger.parseToNode(front)
                while node:
                    '''
                    (
                        pos,
                        subpos,
                        info,
                        subinfo,
                        classification,
                        baseform,
                        word,
                        reading,
                        another_reading
                    ) = node.feature.split(',')
                    '''

                    features = node.feature.split(',')

                    # Skip punctuation marks
                    if len(features) == 9:
                        reading = features[7]
                        if reading != '*':
                            readings.append(reading)
                    node = node.next

                reading = kata2hira(''.join(readings))

                # Save example to DB
                try:
                    example = Example(
                        front=front, reading=reading, gloss=gloss
                    )
                    example.save()
                except Exception:
                    duplicates += 1
                    # self.stdout.write(u'Could not save %s' % front)

            self.stdout.write(
                'Finished saving. Total %d examples prepared! Duplicates: %d' %
                (Example.objects.count(), duplicates)
            )

        # Weblio stuff
        '''
        weblio = Weblio()

        for compound in Compound.objects.all():
            if not compound.is_processed():
                print '[%s]' % compound.front
                examples = weblio.examples(compound.front)
                # Try to exclude items with digits and kana and longer than 3
                for example, gloss in examples.iteritems():
                    print example, gloss
                print '***'
        '''

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
        """Execute command with options specified"""

        # Process kanji info using kanjidic
        if options['kanji']:
            self.update_kanji()

        # Get componds
        if options['compounds']:
            self.update_compounds()

        # Tatoeba and|or weblio for examples
        if options['examples']:
            self.update_examples()

        # Use kradfile to associate kanji with radicals
        if options['radicals']:
            self.update_radicals()
