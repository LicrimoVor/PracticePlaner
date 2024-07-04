from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    author = models.UUIDField()

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=False)
    second_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    mail = models.EmailField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"


@receiver(pre_save, sender=Team)
def set_team_author(sender, instance, *args, **kwargs):
    if not instance.author:
        raise ValueError("Team must have an author.")


class Relationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.team}"


class Task(models.Model):
    STATE_CHOICES = (
        (0, 'Не в работе'),
        (1, 'В работе'),
        (2, 'Завершена'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    deadline = models.DateField(null=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='tasks')
    changeable = models.IntegerField(
        choices=STATE_CHOICES,
        default=0,
        verbose_name='Состояние задачи',
        help_text='0 - Не в работе, 1 - В работе, 2 - Завершена'
    )

    def __str__(self):
        return self.name
