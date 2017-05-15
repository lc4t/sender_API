import json
from django.http import HttpResponse
from express_tracking.func import get_company


def index(request):
    return HttpResponse('/api/function/1/')


def ajax(request):
    response = {
        'status': 1201,
        'message': 'success',
        'data': [
            # 'suda',
            # 'shunfeng',
            # 'yuantong',
        ]
    }
    raw_data = json.loads(request.body.decode())
    number = raw_data.get('input')[0].get('value')
    response['data'] = get_company(number)
    return HttpResponse(json.dumps(response))
