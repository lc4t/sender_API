import json
from celery import shared_task
from celery.schedules import crontab, timedelta
from celery.task import periodic_task
from django.utils.timezone import now
from send_core.models import Task
from django.contrib.auth.models import User
from asyncmailer.tasks import async_select_and_send
from web_change import func


# @periodic_task(run_every=timedelta(seconds=1), name='test')
# def test():
#     print('web_change is running')


@periodic_task(run_every=crontab(minute='*/1'), name='check_new_web_page')
def check_new_web_page():
    tasks = func.get_my_task()
    for t in tasks:
        if t.next_exec <= now() and t.check < 5:
            check_one.delay(t.id)
#
#
@shared_task(default_retry_delay=5, max_retries=3)
def check_one(taskid):
    try:
        new_message = func.check_one(taskid)
        if len(new_message) > 0:
            task = Task.objects.filter(id=taskid)[0]
            title = 'new web change of %s' % task.comment
            plain = json.dumps(new_message, ensure_ascii=False, indent=4)
            async_select_and_send.delay(task.person.email, title, plain)
            func.plus()
    except Exception as e:
        return check_one.retry(taskid)
