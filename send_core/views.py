import json
from send_core.models import Status, Function
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as LOGIN
from django.contrib.auth import logout as LOGOUT
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return HttpResponse('/api/code/index')

def status(request, target):
    response = {
        'status': 100,
        'message': target,
        'data': '',
    }
    status = Status.objects.filter(target=target)
    if len(status) != 1:
        response['data'] = 'cannot pos 1 key'
    else:
        response['data'] = status[0].status
    return HttpResponse(json.dumps(response))

def check_username(username):
    response = {
        'status': 202,
        'message': 'This username is ok.',
    }
    username_black_list = [
        'root', 'admin', 'administrator', 'lc4t',
    ]
    username_black_content = [
        #
    ]
    if not 4 <= len(username) <= 150:
        response['status'] = 410
        response['message'] = 'Hack failed.'
        return response
    if username.lower() in username_black_list:
        response['status'] = 411
        response['message'] = 'This username was banned.'
        return response
    for i in username_black_content:
        if i in username.lower():
            response['status'] = 412
            response['message'] = 'This username was banned.'
            return response
    username_test = User.objects.filter(username=username)
    if len(username_test) > 0:
        response['status'] = 413
        response['message'] = 'This username is exists.'
        return response
    return response


def username_valid(request):
    response = {
        'status': -1,
        'message': 'error',
    }
    if request.method == 'POST':
        raw_data = json.loads(request.body.decode())
        raw_username = raw_data.get('username')
        check = check_username(raw_username)
        response = check
    return HttpResponse(json.dumps(response))

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

def whoami(request):
    response = {
        'status': -1,
        'message': 'error',
        'data': {},
    }
    if request.user.is_authenticated():
        response['status'] = 301
        response['message'] = 'success'
        response['data'] = {
            'username': request.user.username,
            'id': int(request.user.id),
            'email': request.user.email,
        }
    else:
        response['status'] = 401
        response['message'] = 'success'
        response['data'] = {
            'username': None,
            'id': 0,
            'email': None,
        }
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
    elif request.method == 'POST':
        raw_data = json.loads(request.body.decode())
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
            LOGIN(request, user)
            response['status'] = 200
            response['message'] = 'authenticate success'
    return HttpResponse(json.dumps(response))


def logout(request):
    response = {
        'status': -1,
        'message': 'error',
        'data': []
    }
    LOGOUT(request)
    response['status'] = 201
    response['message'] = 'success'
    response['data'] = {
        'username': None,
        'id': 0,
        'email': None,
    }
    return HttpResponse(json.dumps(response))

def register(request):
    pass
