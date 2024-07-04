# serializers.py
from rest_framework import serializers
from .models import User, Team, Task, Relationship


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'


class RelationshipUserSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(source='user.id')

    class Meta:
        model = Relationship
        fields = ['user']

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class RelationshipTeamSerializer(serializers.ModelSerializer):
    team = serializers.UUIDField(source='team.id')

    class Meta:
        model = Relationship
        fields = ['team']

    def get_team(self, obj):
        return TeamSerializer(obj.team).data
