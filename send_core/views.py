import json
from send_core.models import Function
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


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


def login(request):
    response = {
        'status': -1,
        'message': 'error',
        'data': []
    }
    if request.user.is_authenticated():
        response['status'] = 301
        response['message'] = 'already login'
    elif request.POST:
        raw_data = json.loads(request.raw_post_data)
        raw_user = raw_data.get('user')
        raw_password = raw_data.get('password')
        # captcha
        # check which to use
        user = authenticate(username=raw_user, password=raw_password)
        # log this
        if user is None:    # login failed
            response['status'] = 210
            response['message'] = 'authenticate failed'
        else:
            login(request, user)
            response['status'] = 200
            response['message'] = 'authenticate success'
    return HttpResponse(json.dumps(response))

def logout(request):
    pass

def register(request):
    pass
