"""
Context entry models for the Smart Todo application.
"""

from django.db import models


class ContextEntry(models.Model):
    """Model for daily context entries (messages, emails, notes)."""
    
    SOURCE_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('notes', 'Notes'),
        ('calendar', 'Calendar'),
        ('other', 'Other'),
    ]
    
    content = models.TextField(help_text="The actual content of the context entry")
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # AI processing results
    processed_insights = models.JSONField(
        default=dict,
        blank=True,
        help_text="AI-generated insights from context analysis"
    )
    extracted_tasks = models.JSONField(
        default=list,
        blank=True,
        help_text="Tasks extracted from context by AI"
    )
    sentiment_score = models.FloatField(
        null=True,
        blank=True,
        help_text="Sentiment analysis score (-1 to 1)"
    )
    keywords = models.JSONField(
        default=list,
        blank=True,
        help_text="Keywords extracted from context"
    )
    
    # Processing status
    is_processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Context Entry"
        verbose_name_plural = "Context Entries"
    
    def __str__(self):
        return f"{self.get_source_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def preview(self):
        """Return a preview of the content (first 100 characters)."""
        if len(self.content) > 100:
            return self.content[:100] + "..."
        return self.content 