from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Tracking_num(models.Model):   # express nums
    tracking_num = models.CharField(max_length=50, db_index=True)  # lc4t think the express num is not longer than 50
    company = models.CharField(max_length=100)  # so..100
    belongs = models.ForeignKey(User, db_index=True)

    def __str__(self):
        return '%s@%s:%s' % (self.tracking_num, self.company, self.belongs.username)

    class Meta:
        ordering = ['belongs']

    @classmethod
    def create(cls, userid, tracking_num, company):
        belongs = User.objects.filter(id=userid)[0]
        tracking_num = Tracking_num.objects.create(tracking_num=tracking_num, company=company, belongs=belongs)
        return tracking_num


class Tracking(models.Model):
    tracking_num = models.ForeignKey(Tracking_num, db_index=True)
    added_time = models.DateTimeField()
    update_time = models.DateTimeField()
    plain = models.TextField(null=True)

    def __str__(self):
        return '%s[%s]' % (self.tracking_num.tracking_num, str(self.update_time))

    class Meta:
        ordering = ['tracking_num']

    @classmethod
    def create(cls, tracking_num, plain):
        F_Tracking_num = Tracking_num.objects.filter(tracking_num=tracking_num)  # create new tracking
        if len(F_Tracking_num) == 0:    # this tracking num not in Tracking_num
            raise(ValueError('Not exists this Tracking num'))
        else:
            t = now()
            tracking = Tracking.objects.create(tracking_num=F_Tracking_num[0], added_time=t, update_time=t, plain=plain)  # insert new one
            for i in Tracking.objects.filter(tracking_num=F_Tracking_num[0]):
                print(i)
                i.update_time = t
            return tracking
