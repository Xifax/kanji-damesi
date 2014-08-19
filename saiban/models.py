# coding: utf-8
from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from services.srs import interval
from saiban.mecab.BakaMeCab import BakaMeCab

from jcconv import kata2hira

#########################################
# Kanji and related didactical entities #
#########################################


class Kanji(models.Model):
    """Kanji info and associated compounds and components"""

    # Kanji and its relations
    front = models.CharField(max_length=10, unique=True)
    group = models.ForeignKey(  # kanji is unique to group
        'KanjiGroup',
        related_name='kanji',
        null=True,
        blank=True
    )
    radicals = models.ManyToManyField(
        'Radical',
        related_name='kanji',
        null=True,
        blank=True
    )
    compounds = models.ManyToManyField(
        'Compound',
        related_name='kanji',
        null=True,
        blank=True
    )

    # Readings and translations
    on = models.CharField(max_length=100, null=True, blank=True)
    kun = models.CharField(max_length=100, null=True, blank=True)
    nanori = models.CharField(max_length=100, null=True, blank=True)
    gloss = models.CharField(max_length=1000, null=True, blank=True)

    # Additional info
    processed = models.NullBooleanField(default=False, blank=True)
    jlpt = models.PositiveIntegerField(null=True, blank=True)
    grade = models.PositiveIntegerField(null=True, blank=True)
    strokes = models.PositiveIntegerField(null=True, blank=True)
    frequency = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.front

    def as_json(self):
        return dict(
            # main
            id=self.id,
            front=self.front,
            group=str(self.group),
            radicals=[radical.as_json() for radical in self.radicals.all()],
            compounds=[
                compound.as_json() for compound in self.compounds.all()
            ],
            # NB: SRS is not included
            # kanji info
            on=self.on,
            kun=self.kun,
            nanori=self.nanori,
            gloss=self.gloss,
            # additional info
            pocessed=self.processed,
            jlpt=self.jlpt,
            grade=self.grade,
            strokes=self.strokes,
        )

    def get_readings_as_string(self):
        reading = u''
        separator = u' | '
        if self.kun:
            reading += self.kun + separator
        if self.on:
            reading += self.on
        if self.nanori:
            reading += separator + self.nanori

        return reading

    def get_readings_as_json(self):
        readings = {}
        if self.kun:
            readings['kun'] = self.kun
        if self.on:
            readings['on'] = self.on
        if self.nanori:
            readings['nanori'] = self.nanori

        return readings


class Compound(models.Model):
    """Kanji compound, usually word or expression, may include kana"""
    front = models.CharField(max_length=50, unique=True)
    reading = models.CharField(max_length=500, null=True, blank=True)
    gloss = models.CharField(max_length=5000, null=True, blank=True)
    # Part of Speech
    pos = models.CharField(max_length=500, null=True, blank=True)

    examples = models.ManyToManyField(
        'Example',
        related_name='compounds',
        null=True,
        blank=True
    )
    antonyms = models.ManyToManyField('self', null=True, blank=True)
    similar = models.ManyToManyField('self', null=True, blank=True)

    def __unicode__(self):
        return self.front

    def as_json(self):
        return dict(
            front=self.front,
            reading=self.reading,
            gloss=self.gloss,
            examples=[example.as_json() for example in self.examples.all()],
            antonyms=[antonym.as_json() for antonym in self.antonyms.all()],
            similar=[similar.as_json() for similar in self.similar.all()]
        )

    def is_processed(self):
        processed = False
        for kanji in self.kanji.all():
            processed = kanji.processed

        return processed


class Example(models.Model):
    """Example for kanji or compounds"""
    front = models.CharField(max_length=1000, unique=True)
    reading = models.CharField(max_length=1000, null=True, blank=True)
    gloss = models.CharField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.front

    def as_json(self):
        return dict(
            front=self.front,
            reading=self.reading,
            gloss=self.gloss
        )

    def as_mecab(self):
        parser = BakaMeCab(self.front)
        parsed_example = []
        for word, info in parser.get_info().iteritems():
            reading = u''
            if(len(info) > 4):
                kana = info[6] if len(info) > 6 else info[4]
                hiragana = kata2hira(kana)
                if kana != word and hiragana != word and word != 'は':
                    reading = hiragana

            parsed_example.append({'front': word, 'reading': reading})

        return {
            'parsed': parsed_example,
            'original': self.front,
            'reading': self.reading,
            'gloss': self.gloss
        }


class Radical(models.Model):
    """Kanji components, may be identical to kanji for simple ones"""
    front = models.CharField(max_length=10, unique=True)
    info = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    # Additional info
    alternative = models.CharField(max_length=10, null=True, blank=True)
    strokes = models.PositiveIntegerField(null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.front

    def as_json(self):
        return dict(
            front=self.front,
            info=self.info,
            name=self.name,
            # Additional info
            alternative=self.alternative,
            strokes=self.strokes,
            position=self.position
        )


class KanjiGroup(models.Model):
    """Kanji group, associated by radicals, concept or mnemonics"""
    level = models.PositiveIntegerField(default=0)
    info = models.CharField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (
            self.level,
            ' '.join([
                kanji.front for kanji in self.kanji.all()
            ])
        )

    def as_json(self):
        return dict(
            id=self.id,
            level=self.level,
            info=self.info,
            kanji=[kanji.as_json() for kanji in self.kanji.all()]
        )

#################################
# Profile and SRS related stuff #
#################################


class Profile(models.Model):
    """Contains profile studies achivements"""
    EXP = 1  # experience gained for correct answer
    MULTIPLIER = 100  # level-up multiplier

    user = models.ForeignKey(User, related_name='profile')
    group_level = models.PositiveIntegerField(default=1)

    # Vanity info
    vanity_level = models.PositiveIntegerField(default=1)
    day_streak = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
    experience = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(
        upload_to=settings.MEDIA_ROOT,
        null=True,
        blank=True
    )
    achievements = models.ManyToManyField(
        'Achievement',
        related_name='profiles',
        null=True,
        blank=True
    )

    def __unicode__(self):
        return '%s [streak: %d days]' % (self.user.username, self.day_streak)

    def as_json(self):
        return dict(
            level=self.vanity_level,
            streak=self.streak,
            experience=self.experience,
            points=self.EXP,
            multiplier=self.MULTIPLIER
        )


class KanjiStatus(models.Model):
    """Kanji SRS for specific user"""
    # Associated entities: kanji and user
    user = models.ForeignKey(User)
    kanji = models.ForeignKey(  # many (user) statuses for each kanji
        'Kanji',
        related_name='status',
        null=True,
        blank=True
    )
    group_level = models.PositiveIntegerField(default=1, null=True, blank=True)

    # SRS details
    level = models.DecimalField(
        default=0,
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=2
    )
    seen = models.PositiveIntegerField(default=1, null=True, blank=True)
    next_practice = models.DateField(auto_now_add=True)
    easy_factor = models.FloatField(default=2.5)

    def set_next_practice(self, rating):
        """
        Schedule next practice
        Rating may vary from 0 (wtf is this) to 4 (known by heart)
        """
        self.level = rating
        days, ef = interval(self.seen, self.level, self.easy_factor)
        self.next_practice = date.today() + timedelta(days=days)
        self.seen += 1
        self.easy_factor = ef

    def delay(self, days=1):
        """Delay practice for N days"""
        self.next_practice = date.today() + timedelta(days=days)

    def __unicode__(self):
        return u'%s: %s, %s [%s]' % (
            self.kanji,
            str(self.level),
            str(self.easy_factor),
            self.user.username
        )

    def as_json(self):
        return dict(
            kanji=self.kanji.as_json(),
            level=self.level,
            seen=self.seen,
            next_practice=str(self.next_practice),
            easy_factor=self.easy_factor
        )

    def readable_level(self):
        """Get readable level: good, bad, average"""
        if self.level == 4:
            return 'good'
        elif 1 < self.level < 4:
            return 'average'
        elif 0 < self.level <= 1:
            return 'bad'
        else:
            return 'awful'

    class Meta:
        ordering = ['next_practice']


class Achievement(models.Model):
    """Study achievements"""
    description = models.CharField(max_length=1000, unique=True)
    points = models.PositiveIntegerField(default=1, null=True, blank=True)
    icon = models.ImageField(
        upload_to=settings.MEDIA_ROOT,
        null=True,
        blank=True
    )

    def __unicode__(self):
        return '%s [%d]' % (self.description, self.points)


class StudySession(models.Model):
    """Study session for this day (all micro sessions combined)"""
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)

    # Stats
    total_kanji = models.PositiveIntegerField(
        default=0, null=True, blank=True)
    total_errors = models.PositiveIntegerField(
        default=0, null=True, blank=True)
    correct_streak = models.PositiveIntegerField(
        default=0, null=True, blank=True)
    xp_gained = models.PositiveIntegerField(
        default=0, null=True, blank=True)

    # Advanced stats
    last_practice = models.DateTimeField(auto_now_add=True)
    total_time = models.PositiveIntegerField(default=0, null=True, blank=True)

    # Unique kanji number is calculated based on this list
    kanji_studied = models.ManyToManyField(
        'Kanji',
        related_name='sessions',
        null=True,
        blank=True
    )

    def __unicode__(self):
        return '%s [%s] +%sXP' % (
            self.user.username,
            self.date,
            self.xp_gained
        )
