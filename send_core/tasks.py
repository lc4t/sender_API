from celery.schedules import crontab
from celery.task import periodic_task


@periodic_task(run_every=crontab(minute='*/1'), name='send_core_check')
def send_core_check():
    print('send core is running')
