"""
Django admin configuration for context_entries app.
"""

from django.contrib import admin
from .models import ContextEntry


@admin.register(ContextEntry)
class ContextEntryAdmin(admin.ModelAdmin):
    list_display = ['preview', 'source_type', 'timestamp', 'is_processed', 'sentiment_score']
    list_filter = ['source_type', 'is_processed', 'timestamp']
    search_fields = ['content']
    readonly_fields = ['timestamp', 'processed_insights', 'extracted_tasks', 'sentiment_score', 'keywords']
    
    fieldsets = [
        (None, {
            'fields': ['content', 'source_type', 'timestamp']
        }),
        ('AI Processing', {
            'fields': ['is_processed', 'processing_error', 'processed_insights', 'extracted_tasks', 'sentiment_score', 'keywords'],
            'classes': ['collapse']
        })
    ]
    
    def preview(self, obj):
        """Show content preview in admin list."""
        return obj.preview
    preview.short_description = 'Content Preview' 