from django.contrib import admin
from send_core.models import Function, Invite, Invited_user

# Register your models here.
admin.site.register([Function, Invite, Invited_user])
