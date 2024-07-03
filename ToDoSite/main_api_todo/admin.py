from django.contrib import admin
from .models import Team, CustomUser, Relationship, Task

admin.site.register(Team)
admin.site.register(CustomUser)
admin.site.register(Relationship)
admin.site.register(Task)
