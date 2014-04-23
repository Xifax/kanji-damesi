from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication

from models import Kanji, KanjiGroup
from services import (
    get_random_kanji_group,
    get_scheduled_kanji_group
)

############
# Quiz API #
############

class KanjiResource(ModelResource):
    class Meta:
        authentication = SessionAuthentication()
        queryset = Kanji.objects.all()
        resource_name = 'kanji'

    def do_something(self, bundle):
        bundle.request.user

class KanjiGroupResource(ModelResource):
    class Meta:
        authentication = SessionAuthentication()
        queryset = KanjiGroup.objects.all()
        resource_name = 'kanji-group'

class QuizResource(ModelResource):
    class Meta:
        authentication = SessionAuthentication()
        # TODO: use user and get_scheduled_kanji_group
        # queryset = get_random_kanji_group()
        resource_name = 'next-group'

