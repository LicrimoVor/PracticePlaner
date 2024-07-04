from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Team, Task

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'second_name', 'team']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'second_name': 'Отчество'
        }
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'description')
        labels = {
            'name':'Название команды',
            'description':'Описание'
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'deadline', 'team', 'user', 'changeable']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'deadline': 'Скроки',
            'team': 'Команда',
            'user': 'Автор',
            'changeable': 'Изменяемость'
        }