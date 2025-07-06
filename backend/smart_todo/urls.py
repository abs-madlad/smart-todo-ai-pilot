"""
URL configuration for smart_todo project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', include('tasks.urls')),
    path('api/context/', include('context_entries.urls')),
    path('api/ai/', include('ai_integration.urls')),
] 