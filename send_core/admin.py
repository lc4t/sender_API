from django.contrib import admin
from send_core.models import Status, Function, Invite, Invited_user, Task

# Register your models here.
admin.site.register([Status, Function, Invite, Invited_user, Task])
