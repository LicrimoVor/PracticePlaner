# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),

    path('teams/', views.TeamListCreateAPIView.as_view(), name='team-list-create'),
    path('teams/<uuid:pk>/', views.TeamRetrieveUpdateDestroyAPIView.as_view(), name='team-retrieve-update-destroy'),

    path('tasks/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<uuid:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-retrieve-update-destroy'),

    path('user-teams/<uuid:user_id>/', views.UserTeamsListAPIView.as_view(), name='user-teams-list'),
    path('team-tasks/<uuid:team_id>/', views.TeamTasksListAPIView.as_view(), name='team-tasks-list'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path ('profile/', views.profile_view, name = 'profile'),
    path('logout/',  views.login_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('main_page/', views.main_page, name='main_page'),
    path('create-team/', views.create_team_view, name='create_team'),
    path('team-list/', views.team_list_view, name='team_list'),
    path('teams-detail/<uuid:pk>/', views.detail_team_view, name='detail_team_view'),
    path('create-task/', views.create_task_view, name='create_task'),
    path('tasks-list/', views.task_list_view, name='tasks'),
    path('add_user_to_team/', views.add_user_to_team, name='add_user_to_team'),
    path('my-teams/', views.my_teams_view, name='my_teams')
]
