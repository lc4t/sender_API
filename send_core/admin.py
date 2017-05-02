from django.contrib import admin
from send_core.models import Function, Invite_link, Invited_user

# Register your models here.
admin.site.register([Function, Invite_link, Invited_user])
