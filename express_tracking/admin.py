from django.contrib import admin
from express_tracking.models import Tracking, Tracking_num

# Register your models here.
admin.site.register([Tracking, Tracking_num])
