import json
from django.http import HttpResponse


def index(request):
    return HttpResponse('/api/function/1/')


def get_company(request):
    response = {
        'status': 1201,
        'message': 'success',
        'data': [
            'suda',
            'shunfeng',
            'yuantong',
        ]
    }
    print(request.body.decode())
    return HttpResponse(json.dumps(response))


params = {
    "input": [
        {
            "type": "text",
            "name": "number",
            "value": "",
            "descript": "快递单号"
        },
        {
            "type": "text",
            "name": "company",
            "value": "",
            "descript": "快递公司，点击按钮查询，默认为auto"
        }
    ],
    "ajax": {
        "text": "查询公司",
    }
}
