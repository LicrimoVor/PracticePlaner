from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, Team, Task
from .serializers import UserSerializer, TeamSerializer, TaskSerializer

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, UserEditForm, TeamForm, TaskForm, AddUserToTeamForm
from django.contrib.auth.decorators import login_required

# Миксины для User
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# Миксины для Team
class TeamListCreateAPIView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

# Миксины для Task
class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# APIView для получения команд по id пользователя
class UserTeamsListAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            teams = Team.objects.filter(author=user.id)
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# APIView для получения задач по id команды
class TeamTasksListAPIView(APIView):
    def get(self, request, team_id):
        try:
            team = get_object_or_404(Team, id=team_id)
            tasks = Task.objects.filter(team=team)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # URL для перенаправления после регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page')  # URL для перенаправления после входа
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # перенаправление на страницу профиля после успешного сохранения
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def main_page(request):
    return render (request, 'mainpage.html')
@login_required
def create_team_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            author = CustomUser.objects.get(id=request.user.id)
            team.author = author
            team.save()
            team.members.add(request.user)  # Добавляем создателя в члены команды
            return redirect('team_list')  # Перенаправление на список команд или другую страницу
    else:
        form = TeamForm()
    return render(request, 'Createteam.html', {'form': form})
@login_required
def team_list_view (request):
    teams = Team.objects.all()
    return render (request, 'list_teams.html', {'teams': teams})
@login_required
def detail_team_view(request, pk):
    team = get_object_or_404(Team, pk=pk)
    context = {
        'team': team
    }
    return render(request, 'team_detail.html', context)
@login_required
def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            if task.task_type == 'team' and not task.team:
                form.add_error('team', 'Для командной задачи необходимо выбрать команду.')
            else:
                task.save()
                print("ALEALEALEAELAELAEl")
                return redirect('tasks')  # Перенаправьте на список задач или на другую нужную вам страницу
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


def task_list_view(request):
    personal_tasks = Task.objects.filter(created_by=request.user, task_type='personal')
    team_tasks = Task.objects.filter(created_by=request.user, task_type='team')

    print("Personal tasks:", personal_tasks)
    print("Team tasks:", team_tasks)

    return render(request, 'tasks.html', {
        'personal_tasks': personal_tasks,
        'team_tasks': team_tasks,
    })
@login_required
def add_user_to_team(request):
    if request.method == 'POST':
        form = AddUserToTeamForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            team = form.cleaned_data['team']
            team.members.add(user)
            return redirect('detail_team_view', pk=team.pk)
    else:
        form = AddUserToTeamForm()
    return render(request, 'add_user_to_team.html', {'form': form})
@login_required
def my_teams_view(request):
    user_teams = Team.objects.filter(members=request.user)  # Получение всех команд, в которых состоит пользователь
    return render(request, 'my_teams.html', {'user_teams': user_teams})