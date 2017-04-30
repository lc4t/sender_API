from celery.schedules import crontab
from celery.task import periodic_task


@periodic_task(run_every=crontab(minute='*/1'), name='test')
def test():
    print(1)
