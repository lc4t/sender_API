from send_core.models import Task, Function, Log
from web_change.models import Page
from django.utils.timezone import now
import datetime
import json
import re
from urllib.parse import urlparse
import requests as r


def plus():
    functions = Function.objects.filter(name='web_change')
    function = functions[0]
    function.count += 1
    function.save()

def get_my_task():
    functions = Function.objects.filter(name='web_change', status=True)
    if len(functions) == 1:
        function = functions[0]
        tasks = Task.objects.filter(function=function)
        if len(tasks) > 0:
            return tasks
        else:
            return []
    else:
        return []
#
#
def check_one(taskid):
    task = Task.objects.filter(id=taskid)[0]
    params = json.loads(task.params)
    target = params.get('input')[0].get('value')
    match = params.get('input')[1].get('value')
    notmatch = params.get('input')[2].get('value')
    _headers = params.get('input')[3].get('value')

    # check is it in page;
    pages = Page.objects.filter(task=task)
    _ = len(pages)
    if _ >= 2:
        for i in pages:
            i.delete()
        page = Page.objects.create(task=task)
    elif _  == 1:
        page = pages[0]
    else:   # _ == 0
        page = Page.objects.create(task=task)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    if len(_headers) > 0:
        headers = json.loads(_headers)
    _match = page.match
    _notmatch = page.notmatch

    t = urlparse(target)

    if t.scheme not in ['http', 'https'] or len(t.netloc) == 0:
        failed(task)
        Log.objects.create(task=task, text='InvalidURL')
        return []

    try:
        html = r.get(target, headers=headers).text
    except Exception as e:
        failed(task)
        Log.objects.create(task=task, text='Request error %s' % str(e))
        return []

    message = '"{url}" {content}'
    content = ''
    if len(match) == 0:
        content = content + ''
    else:
        if not check_empty(re.findall(match, html)):
            _match = True
            content += '%s is matched' % match
        else:
            _match = False
            # content += '%s is not matched' % match

    if len(notmatch) == 0:
        content = content + ''
    else:
        if not check_empty(re.findall(notmatch, html)):
            _notmatch = True
            # content += '%s is matched' % notmatch
        else:
            _notmatch = False
            content += '%s is not matched' % notmatch
    message = message.format(url=target, content=content)
    success(task)
    Log.objects.create(task=task, text='success' + content)
    if _match != page.match or _notmatch != page.notmatch:
        page.match = _match
        page.notmatch = _notmatch
        page.save()
        return [message]
    else:
        return []

def check_empty(l):
    if l is None:
        return True
    if len(l) == 0:
        return True
    for i in l:
        if len(i) > 0:
            return False
    return True

def failed(task):
    task.last_exec = now()
    task.check += 1
    task.next_exec = now() + datetime.timedelta(minutes= 30 * task.check)
    task.failed += 1
    if 1 <= task.check <= 4:
        task.status = 'failed %d time' % task.check
    else:
        task.status = 'stop'
    task.save()
#
#
def success(task):
    task.status = 'running'
    task.success += 1
    task.check = 0
    task.last_exec = now()
    task.next_exec = now() + datetime.timedelta(minutes=5)
    task.save()
#
#
def delete(task):
    pages = Pages.objects.filter(task=task)
    for page in pages:
        page.delete()
