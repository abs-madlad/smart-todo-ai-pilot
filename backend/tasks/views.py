"""
Django REST Framework views for tasks app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Task, Category
from .serializers import TaskSerializer, TaskCreateSerializer, CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for categories - read-only operations."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        """Filter categories based on query parameters."""
        queryset = Category.objects.all()
        
        # Filter by usage frequency
        min_usage = self.request.query_params.get('min_usage')
        if min_usage:
            queryset = queryset.filter(usage_frequency__gte=min_usage)
        
        return queryset


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for tasks with full CRUD operations."""
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        """Filter tasks based on query parameters."""
        queryset = Task.objects.select_related('category')
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            if priority == 'high':
                queryset = queryset.filter(priority_score__gte=8)
            elif priority == 'medium':
                queryset = queryset.filter(priority_score__gte=6, priority_score__lt=8)
            elif priority == 'low':
                queryset = queryset.filter(priority_score__lt=6)
        
        # Filter by AI suggested
        ai_suggested = self.request.query_params.get('ai_suggested')
        if ai_suggested:
            queryset = queryset.filter(ai_suggested=ai_suggested.lower() == 'true')
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get task statistics."""
        queryset = self.get_queryset()
        
        stats = {
            'total_tasks': queryset.count(),
            'completed_tasks': queryset.filter(status='completed').count(),
            'pending_tasks': queryset.filter(status='pending').count(),
            'in_progress_tasks': queryset.filter(status='in_progress').count(),
            'high_priority_tasks': queryset.filter(priority_score__gte=8, status__in=['pending', 'in_progress']).count(),
            'ai_suggested_tasks': queryset.filter(ai_suggested=True).count(),
            'overdue_tasks': sum(1 for task in queryset if task.is_overdue),
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Toggle task status between pending and completed."""
        task = self.get_object()
        
        if task.status == 'completed':
            task.status = 'pending'
        elif task.status == 'pending':
            task.status = 'completed'
        else:
            task.status = 'completed'
        
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data) 