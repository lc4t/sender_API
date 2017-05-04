from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
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
    user = models.OneToOneField(User, related_name='user', db_index=True)
    person = models.OneToOneField(User, related_name='person', db_index=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s invited %s @%s' % (self.user.username, self.person.username, self.time.strftime('%Y-%m-%d %H:%M:%S'))

    class Meta:
        ordering = ['-time', 'user']
