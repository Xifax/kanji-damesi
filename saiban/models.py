from django.db import models

# Models

class Kanji(models.Model):
    # Kanji and relations
    front = models.CharField(max_length=1)
    # kanji is unique to group
    group = models.ForeignKey(
            'KanjiGroup', related_name='kanji', null=True, blank=True
    )
    radicals = models.ManyToManyField(
            'Radical', related_name='kanji', null=True, blank=True
    )
    compounds = models.ManyToManyField(
            'Compound', related_name='kanji', null=True, blank=True
    )

    # Readings and translations
    on = models.CharField(max_length=100, null=True, blank=True)
    kun = models.CharField(max_length=100, null=True, blank=True)
    namae = models.CharField(max_length=100, null=True, blank=True)
    gloss = models.CharField(max_length=1000, null=True, blank=True)

    # Additional info
    # JLPT, grade, id, etc

    def __unicode__(self):
        return self.front

class Compound(models.Model):
    front = models.CharField(max_length=10)
    reading = models.CharField(max_length=100, null=True, blank=True)
    gloss = models.CharField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return self.front

class Radical(models.Model):
    front = models.CharField(max_length=1)
    info = models.CharField(max_length=100, null=True, blank=True)
    alternative = models.CharField(max_length=1, null=True, blank=True)

    def __unicode__(self):
        return self.front

class KanjiGroup(models.Model):
    level = models.IntegerField(default=0)
    info = models.CharField(max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (
                self.level,
                ' '.join([
                    kanji.front for kanji in self.kanji.all()
                ])
        )

# Managers

class KanjiManager(models.Manager):

    def get_kanji_in_group(self, group):
        pass

class CompoundManager(models.Manager):

    def get_compound_kanji(self, compound):
        pass
