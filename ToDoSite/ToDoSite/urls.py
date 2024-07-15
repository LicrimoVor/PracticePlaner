
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)
from main_api_todo import views

#JWT auth
urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('main_api_todo.urls')),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', views.login_view, name='login'),
]

# swagger
urlpatterns += [
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

