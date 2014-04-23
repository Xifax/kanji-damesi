from django.core import serializers
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

import simplejson as json
import logging

from saiban.services.quiz import (
    get_random_kanji_group,
    get_scheduled_kanji_group
)
from saiban.services.api import json_response, check_request

############
# Quiz API #
############

def random_group(request):
    """Get random kanji group"""
    check_request(request)
    return json_response(get_random_kanji_group().as_json())

def next_group(request):
    """Get next scheduled kanji group"""
    check_request(request)

    # TODO: get scheduled group by level
    group = get_scheduled_kanji_group(request.user)

    # TODO: randomize kanji order
    # TODO get random kanji from group to quiz on
    # TODO: prepare answer and additional info:
    # -> all kanji info
    # -> compounds
    # -> examples

    # Example response
    response = {
        'group': group,
        'quiz': ['meaning', 'reading', 'examples'],
        # If should perform check on client
        'answer': 'kanji',
    }

@csrf_exempt
def process_answer(request):
    """Process user answer"""
    # TODO: may perform this check on client, actually
    # Receives kanji and answer (another kanji), compares with
    # TODO: rate answer
    # TODO: get next group
    pass

@csrf_exempt
def skip_kanji(request):
    """Skip current kanji"""
    # TODO: update kanji srs
    return random_group(request)
