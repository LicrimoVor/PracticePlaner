from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, Team, Task
from .serializers import UserSerializer, TeamSerializer, TaskSerializer

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, UserEditForm
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
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # URL для перенаправления после входа
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
@login_required
def profile_view(request):
    return render(request, 'web/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # перенаправление на страницу профиля после успешного сохранения
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'web/edit_profile.html', {'form': form})