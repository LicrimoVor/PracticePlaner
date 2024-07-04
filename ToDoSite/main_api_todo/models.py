from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver


from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    author = models.UUIDField()
    description = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=False)
    second_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = None
    password = models.CharField(max_length=255, null=False)
    email = models.EmailField(_('email address'), unique = True)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL, related_name='members', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(pre_save, sender=Team)
def set_team_author(sender, instance, *args, **kwargs):
    if not instance.author:
        raise ValueError("Team must have an author.")


class Relationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name='tasks')
    changeable = models.IntegerField(
        choices=STATE_CHOICES,
        default=0,
        verbose_name='Состояние задачи',
        help_text='0 - Не в работе, 1 - В работе, 2 - Завершена'
    )

    def __str__(self):
        return self.name
