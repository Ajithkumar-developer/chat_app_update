from django.contrib import admin
from .models import User, Group, Message, GroupMessage

# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Message)
admin.site.register(GroupMessage)
