"""
Django REST Framework serializers for tasks app.
"""

from rest_framework import serializers
from .models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'usage_frequency', 'created_at']
        read_only_fields = ['usage_frequency', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    priority_level = serializers.CharField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'priority_score', 'priority_level', 'deadline', 'status',
            'ai_suggested', 'ai_insights', 'ai_enhanced_description',
            'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create a new task and update category usage frequency."""
        task = super().create(validated_data)
        if task.category:
            task.category.usage_frequency += 1
            task.category.save()
        return task


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks with AI enhancement."""
    
    category_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'category_name', 'priority_score',
            'deadline', 'status'
        ]
    
    def create(self, validated_data):
        """Create task with category handling."""
        category_name = validated_data.pop('category_name', None)
        
        if category_name:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'usage_frequency': 0}
            )
            validated_data['category'] = category
        
        return super().create(validated_data) 