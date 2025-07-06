"""
Task models for the Smart Todo application.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Model for task categories and tags."""
    name = models.CharField(max_length=100, unique=True)
    usage_frequency = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-usage_frequency', 'name']
    
    def __str__(self):
        return self.name


class Task(models.Model):
    """Model for tasks with AI-powered features."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    priority_score = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Priority score from 1 (low) to 10 (high)"
    )
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # AI-related fields
    ai_suggested = models.BooleanField(default=False)
    ai_insights = models.TextField(blank=True, help_text="AI-generated insights about the task")
    ai_enhanced_description = models.TextField(blank=True, help_text="AI-enhanced task description")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority_score', '-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        """Check if task is overdue."""
        if self.deadline and self.status not in ['completed', 'cancelled']:
            from django.utils import timezone
            return timezone.now() > self.deadline
        return False
    
    @property
    def priority_level(self):
        """Get priority level as string."""
        if self.priority_score >= 8:
            return 'High'
        elif self.priority_score >= 6:
            return 'Medium'
        else:
            return 'Low' 