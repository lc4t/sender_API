import json
import re
from send_core.models import Status, Function, Invite, Invited_user
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as LOGIN
from django.contrib.auth import logout as LOGOUT
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return HttpResponse('/api/code/index')


def check_status(target):
    response = {
        'status': 100,
        'message': target,
        'data': '',
    }
    status = Status.objects.filter(target=target)
    if len(status) != 1:
        response['status'] = 101
        response['data'] = 'cannot pos 1 key'
    else:
        response['data'] = status[0].status
    return response


def status(request, target):
    return HttpResponse(json.dumps(check_status(target)))


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


def check_email(email):
    response = {
        'status': 203,
        'message': 'This email is ok.',
    }
    email_black_list = [

    ]
    email_black_content = [
        #
    ]
    reTest = re.findall('^[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+\.[a-zA-Z]+$', email)
    if len(reTest) != 1:
        response['status'] = 420
        response['message'] = 'Hack failed.'
        return response
    if email.lower() in email_black_list:
        response['status'] = 421
        response['message'] = 'This email was banned.'
        return response
    for i in email_black_content:
        if i in email.lower():
            response['status'] = 422
            response['message'] = 'This email was banned.'
            return response
    email_test = User.objects.filter(email=email)
    if len(email_test) > 0:
        response['status'] = 423
        response['message'] = 'This email is exists.'
        return response
    return response


def check_code(code):
    response = {
        # 'status': 204,
        # 'message': 'This email is ok.',
        'status': -1,
        'message': 'error'
    }
    code_black_list = [

    ]
    code_black_content = [
        #
    ]
    status = check_status('register')
    if 'close' in status['data'] or status['status'] == 101:
        response['status'] = 434
        response['message'] = '关闭注册'
        return response
    elif 'open' in status:
        response['status'] = 435
        response['message'] = '开放注册'
        return response
    # .
    reTest = re.findall('^[a-zA-Z0-9]{40}$', code)
    if len(reTest) != 1:
        response['status'] = 430
        response['message'] = 'Hack failed.'
        return response
    if code in code_black_list:
        response['status'] = 431
        response['message'] = 'This code was banned.'
        return response
    for i in code_black_content:
        if i in code:
            response['status'] = 432
            response['message'] = 'This code was banned.'
            return response
    code_test = Invite.objects.filter(code=code)
    if len(code_test) == 1:
        if code_test[0].remain > 0:
            response['status'] = 204
            response['message'] = 'Invite from %s, %d time(s) remain.' % (code_test[0].user, code_test[0].remain)
            return response
        else:
            response['status'] = 436
            response['message'] = 'Invite from %s, but 0 time remain.' % code_test[0].user
            return response
    else:
        response['status'] = 433
        response['message'] = 'This code is not exists.'
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


def email_valid(request):
    response = {
        'status': -1,
        'message': 'error',
    }
    if request.method == 'POST':
        raw_data = json.loads(request.body.decode())
        raw_email = raw_data.get('email')
        check = check_email(raw_email)
        response = check
    return HttpResponse(json.dumps(response))


def code_valid(request):
    response = {
        'status': -1,
        'message': 'error',
    }
    if request.method == 'POST':
        raw_data = json.loads(request.body.decode())
        raw_code = raw_data.get('code')
        check = check_code(raw_code)
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
    response = {
        'status': -1,
        'message': 'error',
    }
    if request.user.is_authenticated():
        response['status'] = 301
        response['message'] = 'already login'
    elif request.method == 'POST':
        raw_data = json.loads(request.body.decode())
        raw_username = raw_data.get('username')
        raw_password = raw_data.get('password')
        raw_email = raw_data.get('email')
        raw_code = ''

        register_status = check_status('register')
        if 'close' in register_status['data'] or register_status['status'] == 101:
            response['status'] = 501
            response['message'] = '已经关闭注册'
            return HttpResponse(json.dumps(response))
        elif 'invite' in register_status['data']:
            raw_code = raw_data.get('code')
            code_check = check_code(raw_code)
            if code_check['status'] != 204:
                response = code_check
            else:
                response = register_check(raw_username, raw_password, raw_email)
        else:
            response = register_check(raw_username, raw_password, raw_email)

    if response['status'] == 205:
        if 'invite' in check_status('register')['data']:
            invite = Invite.objects.filter(code=raw_code)
            invite = invite[0]
            invite.remain -= 1
            invite.save()
            new_user = User.objects.create_user(raw_username, raw_email, raw_password)
            Invited_user.objects.create(person=new_user, who_invite=invite.user)
        else:
            new_user = User.objects.create_user(raw_username, raw_email, raw_password)
        LOGIN(request, new_user)
    return HttpResponse(json.dumps(response))


def register_check(username, password, email):
    response = {
        'status': 205,
        'message': 'Welcome!'
    }
    username_check = check_username(username)
    if username_check['status'] != 202:
        return username_check
    if username == password:
        return {
            'status': 441,
            'message': 'Hack failed.'
        }
    email_check = check_email(email)
    if email_check['status'] != 203:
        return email_check
    return response
