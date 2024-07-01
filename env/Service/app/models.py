
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Класс Task представляет задачу, которую можно назначить пользователю.

    Атрибуты:
    - title (CharField): Заголовок задачи, ограниченный 200 символами.
    - description (TextField): Подробное описание задачи.
    - deadline (DateTimeField): Срок выполнения задачи.
    - owner (ForeignKey): Владелец задачи, который является пользователем (связан с моделью User).
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Team(models.Model):
    """
    Класс Team представляет команду, состоящую из пользователей.

    Атрибуты:
    - name (CharField): Название команды, ограниченное 100 символами.
    - members (ManyToManyField): Участники команды (связаны с моделью User).
    - owner (ForeignKey): Владелец команды, который является пользователем (связан с моделью User).
    """
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')

    def __str__(self):
        return self.name
