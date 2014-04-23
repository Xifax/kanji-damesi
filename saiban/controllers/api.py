from django.core import serializers
from django.http import HttpResponse, Http404

import simplejson as json
import logging

from saiban.services.quiz import get_random_kanji_group
from saiban.services.api import json_response, check_request

############
# Quiz API #
############

def random_group(request):
    """Get random kanji group"""
    check_request(request)

    group = get_random_kanji_group()
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

