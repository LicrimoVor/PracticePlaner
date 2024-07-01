# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),

    path('teams/', views.TeamListCreateAPIView.as_view(), name='team-list-create'),
    path('teams/<uuid:pk>/', views.TeamRetrieveUpdateDestroyAPIView.as_view(), name='team-retrieve-update-destroy'),

    path('tasks/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<uuid:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-retrieve-update-destroy'),

    path('user-teams/<uuid:user_id>/', views.UserTeamsListAPIView.as_view(), name='user-teams-list'),
    path('team-tasks/<uuid:team_id>/', views.TeamTasksListAPIView.as_view(), name='team-tasks-list'),
]
