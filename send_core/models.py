from django.db import models
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
