from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Team, Task, Relationship
from .serializers import UserSerializer, TeamSerializer, TaskSerializer, \
    RelationshipTeamSerializer, RelationshipUserSerializer, RelationshipSerializer


# Миксины для User
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Миксины для Team
class TeamListCreateAPIView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        team = serializer.save()
        author_id = team.author
        author_user = get_object_or_404(User, id=author_id)
        Relationship.objects.create(user=author_user, team=team)


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
class UserTeamListAPIView(APIView):
    serializer_class = TeamSerializer

    def get(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            teams = Team.objects.filter(author=user.id)
            serializer = self.serializer_class(teams, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# APIView для получения задач по id команды
class TeamTasksListAPIView(APIView):
    serializer_class = TaskSerializer

    def get(self, request, team_id):
        try:
            team = get_object_or_404(Team, id=team_id)
            tasks = Task.objects.filter(team=team)
            serializer = self.serializer_class(tasks, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserTeamsListAPIView(APIView):
    serializer_class = RelationshipTeamSerializer

    def get(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            teams = Relationship.objects.filter(user=user)
            serializer = self.serializer_class(teams, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeamMembersListAPIView(APIView):
    serializer_class = RelationshipUserSerializer

    def get(self, request, team_id):
        try:
            team = get_object_or_404(Team, id=team_id)
            members = Relationship.objects.filter(team=team)
            serializer = self.serializer_class(members, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JoinTeamAPIView(APIView):
    serializer_class = RelationshipSerializer

    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            team_id = request.data.get('team_id')

            if not user_id or not team_id:
                return Response({"detail": "user_id and team_id are required"}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, id=user_id)
            team = get_object_or_404(Team, id=team_id)

            if Relationship.objects.filter(user=user, team=team).exists():
                return Response({"detail": "User already in team"}, status=status.HTTP_400_BAD_REQUEST)

            Relationship.objects.create(user=user, team=team)
            return Response({"detail": "User joined the team"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
