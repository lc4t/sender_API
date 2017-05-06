from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Status(models.Model):
    target = models.CharField(max_length=200, blank=False, db_index=True)
    status = models.CharField(max_length=200, blank=False, default='closed')

    def __str__(self):
        return '%s: %s' % (self.target, self.status)

    class Meta:
        ordering = ['target']


class Function(models.Model):
    name = models.CharField(max_length=200, db_index=True, blank=False)
    author = models.CharField(max_length=200, db_index=True, blank=False)
    title = models.CharField(max_length=200)
    descript = models.TextField()
    count = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    update_time = models.DateTimeField(default=now())

    def __str__(self):
        return '%s@%s:%s' % (self.name, self.author, self.status)

    class Meta:
        ordering = ['name', 'author']


class Invite(models.Model):
    user = models.ForeignKey(User, db_index=True)
    code = models.CharField(max_length=128, db_index=True, default=None)
    link = models.URLField(blank=False)
    remain = models.IntegerField(default=5)

    def __str__(self):
        return '%s %s %d' % (self.user.username, self.link, self.remain)

    class Meta:
        ordering = ['user']


class Invited_user(models.Model):
    person = models.OneToOneField(User, related_name='person', db_index=True)
    who_invite = models.ForeignKey(User, related_name='who_invite', db_index=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s invited %s @%s' % (self.who_invite.username, self.person.username, self.time.strftime('%Y-%m-%d %H:%M:%S'))

    class Meta:
        ordering = ['-time', 'person']
