from django.db import models

# Models

class Kanji(models.Model):
    '''Kanji info and associated compounds and components'''

    # Kanji and its relations
    front = models.CharField(max_length=1, unique=True)
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
    jlpt = models.IntegerField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    strokes = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.front

class Compound(models.Model):
    '''Kanji compound, usually word or expression, may include kana'''
    front = models.CharField(max_length=10, unique=True)
    reading = models.CharField(max_length=100, null=True, blank=True)
    gloss = models.CharField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.front

class Radical(models.Model):
    '''Kanji components, may be identical to kanji for simple ones'''
    front = models.CharField(max_length=1, unique=True)
    info = models.CharField(max_length=100, null=True, blank=True)
    alternative = models.CharField(max_length=1, null=True, blank=True)

    def __unicode__(self):
        return self.front

class KanjiGroup(models.Model):
    '''Kanji group, associated by radicals, concept or mnemonics'''
    level = models.IntegerField(default=0)
    info = models.CharField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (
                self.level,
                ' '.join([
                    kanji.front for kanji in self.kanji.all()
                ])
        )

