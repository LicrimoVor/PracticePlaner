from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Team, CustomUser, Relationship, Task

admin.site.unregister(Group)
admin.site.register(Team)
admin.site.register(CustomUser)
admin.site.register(Relationship)
admin.site.register(Task)

