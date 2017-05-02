import json
from django.http import HttpResponse
from send_core.models import Function


# Create your views here.
def index(request):
    return HttpResponse('/api/code/index')

def get_functions(request):
    results = Function.objects.filter()
    response = []
    for i in results:
        one = {}
        one['name'] = i.name
        one['title'] = i.title
        one['author'] = i.author
        one['descript'] = i.descript
        one['update_time'] = i.update_time.strftime('%Y-%m-%d %H:%M:%S')
        one['count'] = i.count
        one['status'] = i.status
        response.append(one)
    return HttpResponse(json.dumps(response))
