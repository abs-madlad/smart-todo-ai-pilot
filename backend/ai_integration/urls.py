"""
URL patterns for AI integration app.
"""

from django.urls import path
from .views import (
    TaskEnhancementView,
    TaskPrioritizationView,
    ContextAnalysisView,
    AICapabilitiesView
)

urlpatterns = [
    path('enhance-task/', TaskEnhancementView.as_view(), name='enhance-task'),
    path('prioritize-tasks/', TaskPrioritizationView.as_view(), name='prioritize-tasks'),
    path('analyze-context/', ContextAnalysisView.as_view(), name='analyze-context'),
    path('capabilities/', AICapabilitiesView.as_view(), name='ai-capabilities'),
] 