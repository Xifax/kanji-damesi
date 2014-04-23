from django.core import serializers
from django.http import HttpResponse, Http404

import simplejson as json
import logging

from services.quiz import get_random_kanji_group
from services.api import json_response, check_request

############
# Quiz API #
############

def next_group(request):
    check_request(request)

    # TODO: get new group
    group = get_random_kanji_group()
    # for kanji in group.kanji.all():
        # logging.debug(kanji.front)
    # data = simplejson.dumps({'group':group.kanji.all()})
    # kanji = serializers.serialize('json', group.kanji.all())
    # group = serializers.serialize('json', group)
    # response = {'group': {'kanji': kanji, 'data': group}}
    # response = simplejson.dumps({
    #     'group': {'kanji': group.kanji, 'info': group.info}
    # })
    return json_response(group.as_json())

def get_next_quiz(request):
    # TODO: get scheduled group by level
    # TODO: randomize kanji order
    # TODO get random kanji from group to quiz on
    # TODO: prepare answer and additional info:
    # -> all kanji info
    # -> compounds
    # -> examples
    pass

def process_answer(request):
    # TODO: rate answer
    # TODO: get next group
    pass

