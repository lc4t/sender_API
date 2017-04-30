from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sender_API.settings')
app = Celery('send_core', backend='amqp://guest@127.0.0.1//', broker='amqp://guest@127.0.0.1//')
app.conf.update(
    CELERY_ACCEPT_CONTENT = ['application/json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TIMEZONE = 'Asia/Chongqing',
)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


@app.task(bind=True)
def dump_context(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
            self.request))
