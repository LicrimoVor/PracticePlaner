from django.contrib import admin
from .models import Team, User, Relationship, Task

admin.site.register(Team)
admin.site.register(User)
admin.site.register(Relationship)
admin.site.register(Task)
