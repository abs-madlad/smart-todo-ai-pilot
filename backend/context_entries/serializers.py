"""
Django REST Framework serializers for context_entries app.
"""

from rest_framework import serializers
from .models import ContextEntry


class ContextEntrySerializer(serializers.ModelSerializer):
    """Serializer for ContextEntry model."""
    
    preview = serializers.CharField(read_only=True)
    
    class Meta:
        model = ContextEntry
        fields = [
            'id', 'content', 'preview', 'source_type', 'timestamp',
            'processed_insights', 'extracted_tasks', 'sentiment_score',
            'keywords', 'is_processed', 'processing_error'
        ]
        read_only_fields = [
            'timestamp', 'processed_insights', 'extracted_tasks',
            'sentiment_score', 'keywords', 'is_processed', 'processing_error'
        ]


class ContextEntryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating context entries."""
    
    class Meta:
        model = ContextEntry
        fields = ['content', 'source_type']
    
    def create(self, validated_data):
        """Create context entry and trigger AI processing."""
        context_entry = super().create(validated_data)
        
        # Trigger AI processing in the background
        # This would typically be done with Celery or similar
        from .tasks import process_context_entry
        try:
            process_context_entry(context_entry.id)
        except Exception as e:
            context_entry.processing_error = str(e)
            context_entry.save()
        
        return context_entry 