from django.db import models
from django.contrib.auth.models import User
from send_core.models import Task


class Tracking_num(models.Model):   # express nums
    tracking_num = models.CharField(max_length=50, db_index=True)  # lc4t think the express num is not longer than 50
    company = models.CharField(max_length=100)  # so..100
    belongs = models.ForeignKey(User, db_index=True)
    task = models.ForeignKey(Task, db_index=True)

    def __str__(self):
        return '%s@%s:%s' % (self.tracking_num, self.company, self.belongs.username)

    class Meta:
        ordering = ['belongs']

    @classmethod
    def create(cls, belongs, tracking_num, company, task):
        tracking_num = Tracking_num.objects.create(tracking_num=tracking_num, company=company, belongs=belongs, task=task)
        return tracking_num


class Tracking(models.Model):
    tracking_num = models.ForeignKey(Tracking_num, db_index=True)
    # added_time = models.DateTimeField()     # API get
    update_time = models.DateTimeField()
    plain = models.TextField(null=True)

    def __str__(self):
        return '%s[%s] %s' % (self.tracking_num.tracking_num, str(self.update_time), self.plain)

    class Meta:
        ordering = ['tracking_num']
