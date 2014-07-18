from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from saiban.services.quiz import (
    get_random_kanji_group,
    get_scheduled_kanji,
    delay_kanji,
    rate_answer,
    get_examples
)
from saiban.services.api import json_response, check_request, process_post
from saiban.services.user import get_user_level, change_user_level

import random

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
        'group': kanji.group.as_json(),
        'quiz': {
            'meanings': kanji.gloss,
            'readings': kanji.get_readings_as_json(),
            'compounds': [
                compound.as_json() for compound in kanji.compounds.all()
            ],
            'answer': kanji.as_json(),
            'examples': sorted(
                [e.as_mecab() for e in get_examples(kanji.front)],
                key=lambda *args: random.random()
            )
        },
        # TODO: include session/total stats
        'profile': request.user.profile.get().as_json()
    }
    return json_response(response)


@csrf_exempt
def process_answer(request):
    """Process user answer"""
    check_request(request)
    post = process_post(request)

    # NB: this check is performed on the client
    is_correct = post['correct']
    kanji = post['kanji']
    # delay = post['delay']

    rate_answer(kanji, is_correct, request.user)
    # get next group
    return next_group(request)


@csrf_exempt
def skip_kanji(request):
    """Skip current kanji"""
    check_request(request)
    post = process_post(request)

    # Delay kanji by its id
    delay_kanji(post['kanji'], request.user)
    return next_group(request)

###############
# Profile API #
###############


def get_level(request):
    """Get authenticated user level"""
    check_request(request)

    return json_response(get_user_level(request.user))


@csrf_exempt
def change_level(request):
    """Change study level for user"""
    check_request(request)
    post = process_post(request)

    return json_response(change_user_level(request.user, post['level']))
