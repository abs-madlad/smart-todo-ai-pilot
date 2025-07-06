"""
Django admin configuration for tasks app.
"""

from django.contrib import admin
from .models import Task, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'usage_frequency', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['usage_frequency', 'created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority_score', 'status', 'deadline', 'ai_suggested', 'created_at']
    list_filter = ['status', 'priority_score', 'ai_suggested', 'category', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        (None, {
            'fields': ['title', 'description', 'category', 'status']
        }),
        ('Priority & Deadline', {
            'fields': ['priority_score', 'deadline']
        }),
        ('AI Features', {
            'fields': ['ai_suggested', 'ai_insights', 'ai_enhanced_description'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ] 