from django.contrib import admin

# Register your models here.
from django.contrib import admin
from saiban.models import Kanji, KanjiGroup, Compound, Radical

admin.site.register([Kanji, KanjiGroup, Compound, Radical])
