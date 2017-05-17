from django.contrib import admin
from uestc_grade.models import Account, Grade

# Register your models here.
admin.site.register([Account, Grade])
