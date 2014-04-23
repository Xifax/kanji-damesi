from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from services.srs import interval

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
    jlpt = models.IntegerField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    strokes = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.front

    def as_json(self):
        return dict(
            # main
            id=self.id,
            front=self.front,
            group=str(self.group),
            # radicals=[radical.as_json() for radical in self.radicals.all()],
            # compounds=[compound.as_json() for compound in self.compounds.all()],
            # NB:SRS is not included
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

class Compound(models.Model):
    """Kanji compound, usually word or expression, may include kana"""
    front = models.CharField(max_length=10, unique=True)
    reading = models.CharField(max_length=100, null=True, blank=True)
    gloss = models.CharField(max_length=1000, null=True, blank=True)
    examples = models.ManyToManyField(
            'Example',
            related_name='compounds',
            null=True,
            blank=True
    )

    def __unicode__(self):
        return self.front

class Example(models.Model):
    """Example for kanji or compounds"""
    front = models.CharField(max_length=1000, unique=True)
    reading = models.CharField(max_length=1000, null=True, blank=True)
    gloss = models.CharField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.front

class Radical(models.Model):
    """Kanji components, may be identical to kanji for simple ones"""
    front = models.CharField(max_length=10, unique=True)
    info = models.CharField(max_length=100, null=True, blank=True)
    alternative = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return self.front

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
    user = models.ForeignKey(User, related_name='profile')
    group_level = models.PositiveIntegerField(default=0)

    # Vanity info
    vanity_level = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
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
        return '%s [streak: %d days]' % (self.user.username, self.streak)

class KanjiStatus(models.Model):
    """Kanji SRS for specific user"""
    # Associated entities: kanji and user
    user = models.ForeignKey(User)
    kanji = models.ForeignKey( # many (user) statuses for each kanji
            'Kanji',
            related_name='status',
            null=True,
            blank=True
    )

    # SRS details
    level = models.DecimalField(
            default=0,
            null=True,
            blank=True,
            max_digits=3,
            decimal_places=2
    )
    seen = models.PositiveIntegerField(default=0, null=True, blank=True)
    next_practice = models.DateField(auto_now_add=True)
    easy_factor = models.FloatField(default=2.5)

    def set_next_practice(self, rating):
        """
        Schedule next practice
        Rating may vary from 0 (wtf is this) to 4 (known by heart)
        """
        self.level = rating
        days, ef = interval(self.times_practiced, rating, self.easy_factor)
        self.next_practice = date.today() + timedelta(days=days)
        self.times_practiced += 1
        self.easy_factor = ef

    def delay(self, days=1):
        """Delay practice for N days"""
        self.next_practice = date.today() + timedelta(days=days)

    def __unicode__(self):
        return self.level

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
