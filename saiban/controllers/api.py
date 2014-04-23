from django.core import serializers
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

import simplejson as json
import logging

from saiban.services.quiz import (
    get_random_kanji_group,
    get_scheduled_kanji,
    delay_kanji
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

    # get scheduled group for current user by level
    kanji = get_scheduled_kanji(request.user)

    if kanji is None:
        return HttpResponseServerError('Could not get any kanji group.')

    # Prepare response
    response = {
        # TODO: randomize kanji order?
        'group': kanji.group.as_json(),
        'quiz': {
            'meanings': kanji.gloss,
            # TODO: separate fields?
            # 'readings': ', '.join([kanji.kun, kanji.on, kanji.nanori]),
            'readings': kanji.get_reading(),
            'compounds': [compoun.as_json() for compound in kanji.compounds.all()],
            # TODO: ponder what to do
            # 'examples': kanji.compounds.all().examples.all().as_json(),
            'answer': kanji.front,
            'radicals': [],
        },
    }
    return json_response(response)

@csrf_exempt
def process_answer(request):
    """Process user answer"""
    # TODO: may perform this check on client, actually
    # Receives kanji and answer (another kanji), compares with
    # TODO: rate answer
    # TODO: get next group
    return json_response({})

@csrf_exempt
def skip_kanji(request):
    """Skip current kanji"""
    # Delay kanji by its id
    delay_kanji(request.PUT['kanji'])
    return next_group(request)
