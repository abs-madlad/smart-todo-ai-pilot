"""
Django REST Framework views for context_entries app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import ContextEntry
from .serializers import ContextEntrySerializer, ContextEntryCreateSerializer


class ContextEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for context entries with full CRUD operations."""
    
    queryset = ContextEntry.objects.all()
    serializer_class = ContextEntrySerializer
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ContextEntryCreateSerializer
        return ContextEntrySerializer
    
    def get_queryset(self):
        """Filter context entries based on query parameters."""
        queryset = ContextEntry.objects.all()
        
        # Filter by source type
        source_type = self.request.query_params.get('source_type')
        if source_type:
            queryset = queryset.filter(source_type=source_type)
        
        # Filter by processed status
        is_processed = self.request.query_params.get('is_processed')
        if is_processed:
            queryset = queryset.filter(is_processed=is_processed.lower() == 'true')
        
        # Filter by date range
        days_back = self.request.query_params.get('days_back')
        if days_back:
            try:
                days = int(days_back)
                start_date = timezone.now() - timedelta(days=days)
                queryset = queryset.filter(timestamp__gte=start_date)
            except ValueError:
                pass
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search) |
                Q(processed_insights__icontains=search)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get context entry statistics."""
        queryset = self.get_queryset()
        
        # Get stats by source type
        source_stats = queryset.values('source_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Get recent activity (last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        recent_count = queryset.filter(timestamp__gte=week_ago).count()
        
        # Get processing stats
        processed_count = queryset.filter(is_processed=True).count()
        total_count = queryset.count()
        
        stats = {
            'total_entries': total_count,
            'processed_entries': processed_count,
            'processing_rate': round((processed_count / total_count * 100) if total_count > 0 else 0, 2),
            'recent_entries': recent_count,
            'source_breakdown': list(source_stats),
            'avg_sentiment': queryset.exclude(sentiment_score__isnull=True).aggregate(
                avg_sentiment=Avg('sentiment_score')
            )['avg_sentiment'] or 0,
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        """Reprocess a context entry with AI."""
        context_entry = self.get_object()
        
        try:
            from .tasks import process_context_entry
            process_context_entry(context_entry.id)
            return Response({'status': 'processing started'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def insights(self, request):
        """Get aggregated insights from all context entries."""
        queryset = self.get_queryset().filter(is_processed=True)
        
        # Collect all insights
        all_insights = []
        all_keywords = []
        
        for entry in queryset:
            if entry.processed_insights:
                all_insights.extend(entry.processed_insights.get('insights', []))
            if entry.keywords:
                all_keywords.extend(entry.keywords)
        
        # Count keyword frequency
        from collections import Counter
        keyword_freq = Counter(all_keywords)
        
        insights_data = {
            'total_insights': len(all_insights),
            'top_keywords': keyword_freq.most_common(10),
            'recent_insights': all_insights[-10:] if all_insights else [],
        }
        
        return Response(insights_data) 