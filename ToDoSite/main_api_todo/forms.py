from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Team, Task

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
    labels = {
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'second_name': 'Отчество'
    }


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

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

class AddUserToTeamForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Пользователь")
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Команда")

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']