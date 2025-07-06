"""
Django app configuration for context entries.
"""

from django.apps import AppConfig


class ContextEntriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'context_entries'
    verbose_name = 'Context Entries' 