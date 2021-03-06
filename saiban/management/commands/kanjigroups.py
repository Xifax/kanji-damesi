# coding: utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from saiban.models import Kanji, KanjiGroup

from optparse import make_option
import json

from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--json',
                    action='store_true',
                    dest='json',
                    default=False,
                    help='Dump json instead of importing entities to database'
                    ),
        make_option('--update',
                    action='store_true',
                    dest='update',
                    default=False,
                    help='Update groups info'),
    )
    help = 'Populates database|dumps json data with kanji and kanji groups'
    base_url = (
        'http://www.coscom.co.jp/ebksample/'
        'smp_2001kanji301/menumm/menubody-level%d-%d.html'
    )
    levels = {
        1: 5,
        1: 5,
        2: 5,
        3: 5,
        4: 3,
    }

    def handle(self, *args, **options):
        # prepare list of kanji and groups
        kanji_groups = []
        for level, subsections in self.levels.items():
            self.stdout.write('Processing level %d' % level)
            for section in range(subsections):
                self.stdout.write('Processing section %d' % int(section + 1))
                url = self.base_url % (level, section + 1)
                try:
                    # set encoding manually
                    response = requests.get(url)
                    response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.text)

                    # div with groups, group subtitles and group tables
                    main = soup.find('div', class_='menuhonbun')
                    glosses = main.find_all('p', class_='grpimi')
                    glosses.reverse()
                    groups = main.find_all('table', class_='group')

                    # compose list of kanji groups
                    for group in groups:
                        kanji_groups.append({
                            'level': level,
                            'kanji': [
                                kanji.get_text() for kanji in
                                group.find_all('td', class_='listKanji')
                            ],
                            'info': glosses.pop().get_text()
                        })

                except Exception as e:
                    raise CommandError(
                        'Could not process url: %s (%s)' % (url, e)
                    )

        # either dump resulting data to json
        if options['json']:
            self.stdout.write(json.dumps(kanji_groups))

        # update group info
        elif options['update']:
            for group in KanjiGroup.objects.all():
                if kanji_groups:
                    # get next updated group
                    update = kanji_groups.pop(0)
                    # skip this particular group
                    if '々' in update['kanji']:
                        update = kanji_groups.pop(0)

                    # update group in DB
                    group.info = update['info']
                    group.save()

        # or save to database as corresponding entities
        else:
            self.stdout.write('Filling up the database')
            for group in kanji_groups:
                # self.stdout.write(
                #         '\r[{0}] {1}%'.format('#'*(progress/10), progress)
                # )
                kanji_group = KanjiGroup(
                    level=group['level'],
                    info=group['info']
                )
                kanji_group.save()

                for kanji in group['kanji']:
                    new_kanji = Kanji(front=kanji, group=kanji_group)
                    try:
                        new_kanji.save()
                    except Exception as e:
                        self.stdout.write(
                            'Could not save kanji %s [%s]' % (kanji, e)
                        )

        self.stdout.write('Done!')
