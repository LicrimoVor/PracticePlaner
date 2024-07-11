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


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class TeamListCreateAPIView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserTeamsListAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            teams = Team.objects.filter(author=user.id)
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            return redirect('login')
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
                return redirect('profile')
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
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'web/edit_profile.html', {'form': form})


def main_page(request):
    return render (request, 'web/mainpage.html')
@login_required
def create_team_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.author = request.user.id
            team.save()
            return redirect('main_page')
    else:
        form = TeamForm()
    return render(request, 'web/create_team.html', {'form': form})
@login_required
def team_list_view (request):
    teams = Team.objects.all()
    return render (request, 'web/list_teams.html', {'teams': teams})
@login_required
def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('task-list-create')
    else:
        form = TaskForm()
    return render(request, 'web/create_task.html', {'form': form})

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
    return render(request, 'web/add_user_to_team.html', {'form': form})

def detail_team_view(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('detail_team_view', pk=team.pk)
    else:
        form = TeamForm(instance=team)
    return render(request, 'web/team_detail.html', {'team': team, 'form': form})