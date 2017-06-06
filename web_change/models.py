from django.db import models
from django.contrib.auth.models import User
from send_core.models import Task


class Page(models.Model):
    task = models.ForeignKey(Task, db_index=True)
    match = models.BooleanField(default=False)
    notmatch = models.BooleanField(default=True)


    def __str__(self):
        return '%s' % (self.task.id)
