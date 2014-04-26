from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from saiban.services.quiz import (
    get_random_kanji_group,
    get_scheduled_kanji,
    delay_kanji,
    rate_answer
)
from saiban.services.api import json_response, check_request, process_post

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
            # TODO: separate kun|on|nanori fields?
            'readings': kanji.get_reading(),
            'compounds': [
                compound.as_json() for compound in kanji.compounds.all()
            ],
            # TODO: ponder what to do
            # 'examples': kanji.compounds.all().examples.all().as_json(),
            'answer': kanji.front,
            # 'radicals': [
            #   radical.as_json() for radical in kanji.radicals.all()
            # ],
        },
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
    delay = post['delay']

    rate_answer(kanji, is_correct)
    # get next group
    return next_group(request)


@csrf_exempt
def skip_kanji(request):
    """Skip current kanji"""
    # Delay kanji by its id
    delay_kanji(request.PUT['kanji'])
    return next_group(request)
