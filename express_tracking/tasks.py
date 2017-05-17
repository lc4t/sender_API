import json
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from express_tracking import func
from django.utils.timezone import now
from send_core.models import Task
from django.contrib.auth.models import User
from asyncmailer.tasks import async_select_and_send


# @periodic_task(run_every=crontab(minute='*/1'), name='test')
# def test():
#     print('express_tracking is running')


@periodic_task(run_every=crontab(minute='*/1'), name='check_new_express')
def check_new_express():
    tasks = func.get_my_task()
    for t in tasks:
        if t.next_exec <= now() and t.check < 5:
            try:
                person = t.person
                params = json.loads(t.params)
                number = params.get('input')[0].get('value')
                company = params.get('input')[1].get('value')
                check_one.delay(number, company, person.id, t.id)
            except Exception as e:
                pass


@shared_task(default_retry_delay=5, max_retries=3)
def get_all_message(number, company):
    try:
        return func.get_all_message(number, company)
    except Exception as e:
        return get_all_message.retry(number, company)


@shared_task(default_retry_delay=5, max_retries=3)
def check_one(number, company, personid, taskid):
    try:
        new_message = func.check_one(number, company, personid, taskid)
        for i in new_message:
            title = 'new express tracking of %s' % Task.objects.filter(id=taskid)[0].comment
            plain = '%s %s update @%s: %s' % (company, number, i.get('time'), i.get('text'))
            async_select_and_send.delay(User.objects.filter(id=personid)[0].email, title, plain)
            func.plus()
    except Exception as e:
        return check_one.retry(number, company, personid, taskid)
