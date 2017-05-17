from django.db import models
from django.contrib.auth.models import User
from send_core.models import Task


class Account(models.Model):
    username = models.CharField(max_length=50, db_index=True)  # lc4t think the express num is not longer than 50
    password = models.CharField(max_length=100)  # so..100
    cookie = models.CharField(max_length=200, default='')
    belongs = models.ForeignKey(User, db_index=True)
    task = models.ForeignKey(Task, db_index=True)

    def __str__(self):
        return '%s:%s' % (self.task.id, self.username)

    class Meta:
        ordering = ['username', 'belongs']


class Grade(models.Model):
    account = models.ForeignKey(Account, db_index=True)
    update_time = models.DateTimeField(auto_now_add=True)
    academisc = models.CharField(max_length=20, default='', db_index=True)
    semester = models.CharField(max_length=2, default='', db_index=True)
    courseCode = models.CharField(max_length=30, default='', db_index=True)
    number = models.CharField(max_length=30, default='', db_index=True)
    courseName = models.CharField(max_length=100, default='')
    courseType = models.CharField(max_length=100, default='')
    credit = models.CharField(max_length=2, default='')
    totalGrade = models.CharField(max_length=8, default='', db_index=True)
    makeupGrade = models.CharField(max_length=8, default='', db_index=True)
    finalGrade = models.CharField(max_length=8, default='', db_index=True)
    gradePoint = models.CharField(max_length=8, default='')

    def __str__(self):
        return '%s[%s] %s' % (self.account.username, self.update_time.strftime('%Y-%m-%d %H:%M:%S'), self.courseName)

    class Meta:
        ordering = ['account', 'update_time']
