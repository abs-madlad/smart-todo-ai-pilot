"""
AI Integration API views.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .services import AIService
from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskEnhancementView(APIView):
    """API view for AI-powered task enhancement."""
    
    def post(self, request):
        """Enhance a task with AI suggestions."""
        try:
            data = request.data
            title = data.get('title', '')
            description = data.get('description', '')
            category = data.get('category', '')
            
            if not title:
                return Response(
                    {'error': 'Title is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ai_service = AIService()
            enhancement = ai_service.enhance_task(title, description, category)
            
            return Response(enhancement)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskPrioritizationView(APIView):
    """API view for AI-powered task prioritization."""
    
    def post(self, request):
        """Prioritize a list of tasks using AI."""
        try:
            task_ids = request.data.get('task_ids', [])
            
            if not task_ids:
                return Response(
                    {'error': 'task_ids list is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get tasks from database
            tasks = Task.objects.filter(id__in=task_ids)
            task_data = []
            
            for task in tasks:
                task_data.append({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'category': task.category.name if task.category else None,
                    'current_priority': task.priority_score,
                    'deadline': task.deadline.isoformat() if task.deadline else None
                })
            
            # Prioritize with AI
            ai_service = AIService()
            prioritized_tasks = ai_service.prioritize_tasks(task_data)
            
            # Update tasks in database
            for task_data in prioritized_tasks:
                task = tasks.get(id=task_data['id'])
                if 'priority_score' in task_data:
                    task.priority_score = task_data['priority_score']
                    task.ai_insights = f"Priority updated by AI: {task_data.get('reasoning', '')}"
                    task.save()
            
            # Return updated tasks
            updated_tasks = Task.objects.filter(id__in=task_ids)
            serializer = TaskSerializer(updated_tasks, many=True)
            
            return Response({
                'prioritized_tasks': serializer.data,
                'reasoning': 'Tasks prioritized using AI analysis'
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContextAnalysisView(APIView):
    """API view for context analysis."""
    
    def post(self, request):
        """Analyze context content and extract insights."""
        try:
            content = request.data.get('content', '')
            source_type = request.data.get('source_type', 'notes')
            
            if not content:
                return Response(
                    {'error': 'Content is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ai_service = AIService()
            analysis = ai_service.analyze_context(content, source_type)
            
            return Response(analysis)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AICapabilitiesView(APIView):
    """API view to check AI capabilities and status."""
    
    def get(self, request):
        """Get information about available AI providers."""
        from django.conf import settings
        
        capabilities = {
            'available_providers': [],
            'features': {
                'context_analysis': True,
                'task_enhancement': True,
                'task_prioritization': True,
                'sentiment_analysis': True,
                'keyword_extraction': True
            },
            'status': 'operational'
        }
        
        # Check available providers
        if settings.LM_STUDIO_BASE_URL:
            capabilities['available_providers'].append({
                'name': 'LM Studio',
                'type': 'local',
                'status': 'available'
            })
        
        if settings.ANTHROPIC_API_KEY:
            capabilities['available_providers'].append({
                'name': 'Anthropic Claude',
                'type': 'cloud',
                'status': 'available'
            })
        
        if settings.OPENAI_API_KEY:
            capabilities['available_providers'].append({
                'name': 'OpenAI GPT',
                'type': 'cloud',
                'status': 'available'
            })
        
        if not capabilities['available_providers']:
            capabilities['available_providers'].append({
                'name': 'Rule-based Fallback',
                'type': 'local',
                'status': 'available'
            })
        
        return Response(capabilities) 