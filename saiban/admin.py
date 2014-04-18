from django.contrib import admin

# Register your models here.
from django.contrib import admin
from saiban.models import Kanji, KanjiGroup, Compound, Radical


class KanjiAdmin(admin.ModelAdmin):
    search_fields = ['front']

class CompoundAdmin(admin.ModelAdmin):
    search_fields = ['front']

admin.site.register(Kanji, KanjiAdmin)
admin.site.register(Compound, CompoundAdmin)

admin.site.register([Radical, KanjiGroup])
