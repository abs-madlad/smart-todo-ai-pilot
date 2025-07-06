"""
AI processing tasks for context entries.
"""

import json
import re
from django.conf import settings
from .models import ContextEntry


def process_context_entry(context_entry_id):
    """Process a context entry with AI to extract insights and tasks."""
    try:
        context_entry = ContextEntry.objects.get(id=context_entry_id)
        
        # Import AI integration
        from ai_integration.services import AIService
        ai_service = AIService()
        
        # Process the context content
        analysis_result = ai_service.analyze_context(
            content=context_entry.content,
            source_type=context_entry.source_type
        )
        
        # Update context entry with results
        context_entry.processed_insights = analysis_result.get('insights', {})
        context_entry.extracted_tasks = analysis_result.get('extracted_tasks', [])
        context_entry.sentiment_score = analysis_result.get('sentiment_score')
        context_entry.keywords = analysis_result.get('keywords', [])
        context_entry.is_processed = True
        context_entry.processing_error = ''
        
        context_entry.save()
        
        # Auto-create high-priority tasks if found
        auto_create_tasks_from_context(context_entry, analysis_result)
        
    except ContextEntry.DoesNotExist:
        print(f"Context entry {context_entry_id} not found")
    except Exception as e:
        try:
            context_entry = ContextEntry.objects.get(id=context_entry_id)
            context_entry.processing_error = str(e)
            context_entry.is_processed = False
            context_entry.save()
        except:
            pass
        print(f"Error processing context entry {context_entry_id}: {e}")


def auto_create_tasks_from_context(context_entry, analysis_result):
    """Auto-create tasks from high-priority context analysis."""
    from tasks.models import Task, Category
    
    extracted_tasks = analysis_result.get('extracted_tasks', [])
    
    for task_data in extracted_tasks:
        # Only auto-create high-priority tasks
        if task_data.get('priority', 0) >= 8:
            try:
                # Get or create category
                category = None
                if task_data.get('category'):
                    category, created = Category.objects.get_or_create(
                        name=task_data['category'],
                        defaults={'usage_frequency': 0}
                    )
                
                # Create task
                task = Task.objects.create(
                    title=task_data.get('title', 'Untitled Task'),
                    description=task_data.get('description', ''),
                    category=category,
                    priority_score=task_data.get('priority', 8),
                    deadline=task_data.get('deadline'),
                    ai_suggested=True,
                    ai_insights=f"Auto-created from {context_entry.get_source_type_display()} context analysis"
                )
                
                # Update category usage
                if category:
                    category.usage_frequency += 1
                    category.save()
                    
            except Exception as e:
                print(f"Error creating task from context: {e}")


def extract_keywords(text):
    """Simple keyword extraction from text."""
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
    }
    
    # Extract words (basic approach)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    keywords = [word for word in words if word not in stop_words]
    
    # Return most frequent keywords
    from collections import Counter
    word_freq = Counter(keywords)
    return [word for word, count in word_freq.most_common(10)] 