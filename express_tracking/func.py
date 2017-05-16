import json
from random import randint
import datetime
import requests as r
from send_core.models import Task, Function, Log
from django.utils.timezone import now
from django.contrib.auth.models import User
from express_tracking.models import Tracking_num, Tracking


headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Chrome/%d.%d.%d.%d' % (randint(100, 1000), randint(0, 9), randint(1000, 9999), randint(100, 999)),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.8',
}


def get_company(number):
    url = 'https://www.kuaidi100.com/autonumber/autoComNum?text=%s' % number
    getter = r.get(url, headers=headers).text
    message = json.loads(getter)
    company = []
    for i in message.get('auto'):
        company.append(i.get('comCode'))
    return company


def plus():
    functions = Function.objects.filter(name='express_tracking')
    function = functions[0]
    function.count += 1
    function.save()


def get_my_task():
    # global ID
    functions = Function.objects.filter(name='express_tracking', status=True)
    if len(functions) == 1:
        function = functions[0]
        tasks = Task.objects.filter(function=function)
        if len(tasks) > 0:
            return tasks
        else:
            return []
    else:
        return []


def failed(task):
    task.last_exec = now()
    task.next_exec = now() + datetime.timedelta(minutes=5)
    task.check += 1
    task.failed += 1
    if 1 <= task.check <= 4:
        task.status = 'failed %d time' % task.check
    else:
        task.status = 'stop'
    task.save()


def success(message, tracking_num, task):
    data = []
    new_message = []
    for i in message.get('data', []):
        context = i.get('context')
        t = i.get('time')
        if context is not None or t is not None:
            data.append({
                'time': t,
                'text': context,
            })
    data = sorted(data, key=lambda obj: obj.get('time'))
    for d in data:
        t = d.get('time')
        ttime = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        checker = Tracking.objects.filter(tracking_num=tracking_num, update_time=ttime, plain=d.get('text'))
        if len(checker) == 0:
            Tracking.objects.create(tracking_num=tracking_num, update_time=ttime, plain=d.get('text'))
            new_message.append(d)
    task.status = 'running'
    task.success += 1
    task.check = 0
    task.last_exec = now()
    task.next_exec = now() + datetime.timedelta(minutes=5)
    task.save()
    return new_message


def check():
    tasks = get_my_task()
    for task in tasks:
        if task.next_exec <= now():
            check_one(task)


def get_all_message(number, company):
    url = 'https://www.kuaidi100.com/query?type=%s&postid=%s' % (company, number)
    try:
        getter = r.get(url, headers=headers).text
        message = json.loads(getter)
    except Exception as e:
        message = {'error': 'get message from %s' % url}
    return message


def check_one(number, company, personid, taskid):
    task = Task.objects.filter(id=taskid)[0]
    user = User.objects.filter(id=personid)[0]
    exists = Tracking_num.objects.filter(tracking_num=number, company=company, belongs=user)
    if len(exists) == 0:
        tracking_num = Tracking_num.create(user, number, company, task)
    else:
        tracking_num = exists[0]
    message = get_all_message(number, company)
    text = json.dumps(message, ensure_ascii=False)
    if len(Log.objects.filter(task=task, text=text)) > 0:
        text = 'same with last one'
    Log.objects.create(task=task, text=text)
    # check message

    if message['status'] == '400':
        failed(task)
    elif message['status'] in ['200', '201']:
        new_message = success(message, tracking_num, task)
        return new_message
    elif message is None:
        print('server error')
    else:
        print(message)
    return []


def delete(task):
    tracking_nums = Tracking_num.objects.filter(task=task)
    for tracking_num in tracking_nums:
        delete_tracking(tracking_num)
        tracking_num.delete()

def delete_tracking(tracking_num):
    trackings = Trackings.objects.filter(tracking_num=tracking_num)
    for tracking in trackings:
        tracking.delete()
