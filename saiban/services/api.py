from django.http import HttpResponse, Http404
import simplejson

# API utils


def json_response(data):
    """Return json-encoded response"""
    return HttpResponse(
        simplejson.dumps(data),
        mimetype='application/json'
    )


def check_request(request):
    """Check if AJAX request from authenticated user"""
    if not request.user.is_authenticated():
        raise Http404

    # if not request.is_ajax():
    #     raise Http404


def process_post(request):
    if (
        'CONTENT_TYPE' in request.META and
        request.META['CONTENT_TYPE'].startswith('application/json')
    ):
        return simplejson.loads(request.body)
    elif request.method == 'POST':
        return request.POST.dict()
