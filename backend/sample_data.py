#!/usr/bin/env python3
"""
Sample data creation script for Smart Todo AI Application
Run this script to populate the database with sample data for testing.
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_todo.settings')
django.setup()

from tasks.models import Task, Category
from context_entries.models import ContextEntry

def create_categories():
    """Create sample categories."""
    categories_data = [
        {'name': 'Work', 'usage_frequency': 15},
        {'name': 'Personal', 'usage_frequency': 10},
        {'name': 'Health', 'usage_frequency': 8},
        {'name': 'Shopping', 'usage_frequency': 6},
        {'name': 'Education', 'usage_frequency': 5},
        {'name': 'Finance', 'usage_frequency': 4},
        {'name': 'Home', 'usage_frequency': 7},
        {'name': 'Travel', 'usage_frequency': 3},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'usage_frequency': cat_data['usage_frequency']}
        )
        categories.append(category)
        if created:
            print(f"✅ Created category: {category.name}")
    
    return categories

def create_tasks(categories):
    """Create sample tasks."""
    tasks_data = [
        {
            'title': 'Complete project presentation',
            'description': 'Prepare slides for quarterly review meeting with stakeholders',
            'category': 'Work',
            'priority_score': 9,
            'deadline': timezone.now() + timedelta(days=2),
            'status': 'pending',
            'ai_suggested': True,
            'ai_insights': 'High priority based on upcoming deadline and email context'
        },
        {
            'title': 'Buy groceries',
            'description': 'Weekly grocery shopping - milk, bread, eggs, vegetables',
            'category': 'Shopping',
            'priority_score': 5,
            'deadline': timezone.now() + timedelta(days=1),
            'status': 'pending',
            'ai_suggested': False,
        },
        {
            'title': 'Schedule dentist appointment',
            'description': 'Annual dental checkup and cleaning',
            'category': 'Health',
            'priority_score': 6,
            'deadline': timezone.now() + timedelta(days=14),
            'status': 'completed',
            'ai_suggested': True,
            'ai_insights': 'Suggested based on calendar analysis and health reminders'
        },
        {
            'title': 'Review budget and expenses',
            'description': 'Monthly financial review and budget planning',
            'category': 'Finance',
            'priority_score': 7,
            'deadline': timezone.now() + timedelta(days=5),
            'status': 'pending',
            'ai_suggested': False,
        },
        {
            'title': 'Learn Python data structures',
            'description': 'Complete online course module on advanced data structures',
            'category': 'Education',
            'priority_score': 4,
            'deadline': timezone.now() + timedelta(days=21),
            'status': 'in_progress',
            'ai_suggested': True,
            'ai_insights': 'Learning goal identified from notes analysis'
        },
        {
            'title': 'Fix leaky faucet',
            'description': 'Repair the kitchen faucet that has been dripping',
            'category': 'Home',
            'priority_score': 6,
            'deadline': timezone.now() + timedelta(days=7),
            'status': 'pending',
            'ai_suggested': False,
        },
        {
            'title': 'Plan weekend trip',
            'description': 'Research and book accommodation for weekend getaway',
            'category': 'Travel',
            'priority_score': 3,
            'deadline': timezone.now() + timedelta(days=10),
            'status': 'pending',
            'ai_suggested': True,
            'ai_insights': 'Travel planning detected from conversation context'
        },
        {
            'title': 'Prepare tax documents',
            'description': 'Gather all necessary documents for tax filing',
            'category': 'Finance',
            'priority_score': 8,
            'deadline': timezone.now() + timedelta(days=30),
            'status': 'pending',
            'ai_suggested': False,
        },
        {
            'title': 'Team meeting preparation',
            'description': 'Prepare agenda and materials for weekly team meeting',
            'category': 'Work',
            'priority_score': 7,
            'deadline': timezone.now() + timedelta(days=3),
            'status': 'pending',
            'ai_suggested': True,
            'ai_insights': 'Meeting detected in calendar with preparation needed'
        },
        {
            'title': 'Exercise routine',
            'description': 'Maintain daily 30-minute exercise routine',
            'category': 'Health',
            'priority_score': 5,
            'deadline': timezone.now() + timedelta(days=1),
            'status': 'completed',
            'ai_suggested': False,
        }
    ]
    
    category_map = {cat.name: cat for cat in categories}
    
    for task_data in tasks_data:
        category = category_map.get(task_data['category'])
        
        task, created = Task.objects.get_or_create(
            title=task_data['title'],
            defaults={
                'description': task_data['description'],
                'category': category,
                'priority_score': task_data['priority_score'],
                'deadline': task_data['deadline'],
                'status': task_data['status'],
                'ai_suggested': task_data['ai_suggested'],
                'ai_insights': task_data.get('ai_insights', ''),
            }
        )
        
        if created:
            print(f"✅ Created task: {task.title}")

def create_context_entries():
    """Create sample context entries."""
    context_data = [
        {
            'content': 'Meeting with client tomorrow at 3 PM. Need to prepare the quarterly report and presentation slides.',
            'source_type': 'whatsapp',
            'processed_insights': {
                'summary': 'Client meeting detected with preparation tasks',
                'urgency_level': 'high',
                'task_count': 2
            },
            'extracted_tasks': [
                {
                    'title': 'Prepare quarterly report',
                    'priority': 9,
                    'category': 'Work',
                    'deadline': '2025-01-05T15:00:00Z'
                },
                {
                    'title': 'Create presentation slides',
                    'priority': 8,
                    'category': 'Work',
                    'deadline': '2025-01-05T15:00:00Z'
                }
            ],
            'sentiment_score': 0.1,
            'keywords': ['meeting', 'client', 'quarterly', 'report', 'presentation'],
            'is_processed': True
        },
        {
            'content': 'Reminder: Annual performance reviews are due by January 15th. Please submit your self-assessment.',
            'source_type': 'email',
            'processed_insights': {
                'summary': 'Performance review deadline identified',
                'urgency_level': 'medium',
                'task_count': 1
            },
            'extracted_tasks': [
                {
                    'title': 'Complete self-assessment for performance review',
                    'priority': 7,
                    'category': 'Work',
                    'deadline': '2025-01-15T17:00:00Z'
                }
            ],
            'sentiment_score': 0.0,
            'keywords': ['performance', 'review', 'deadline', 'assessment'],
            'is_processed': True
        },
        {
            'content': 'Don\'t forget to buy groceries tomorrow. Need milk, bread, eggs, and vegetables for the week.',
            'source_type': 'notes',
            'processed_insights': {
                'summary': 'Shopping list and reminder identified',
                'urgency_level': 'low',
                'task_count': 1
            },
            'extracted_tasks': [
                {
                    'title': 'Buy groceries',
                    'priority': 5,
                    'category': 'Shopping',
                    'deadline': '2025-01-06T18:00:00Z'
                }
            ],
            'sentiment_score': 0.0,
            'keywords': ['groceries', 'milk', 'bread', 'eggs', 'vegetables'],
            'is_processed': True
        },
        {
            'content': 'Dentist appointment scheduled for next week. Also need to call insurance about coverage.',
            'source_type': 'whatsapp',
            'processed_insights': {
                'summary': 'Health-related tasks identified',
                'urgency_level': 'medium',
                'task_count': 2
            },
            'extracted_tasks': [
                {
                    'title': 'Attend dentist appointment',
                    'priority': 6,
                    'category': 'Health',
                    'deadline': '2025-01-12T10:00:00Z'
                },
                {
                    'title': 'Call insurance about dental coverage',
                    'priority': 5,
                    'category': 'Health',
                    'deadline': '2025-01-08T16:00:00Z'
                }
            ],
            'sentiment_score': 0.0,
            'keywords': ['dentist', 'appointment', 'insurance', 'coverage'],
            'is_processed': True
        },
        {
            'content': 'Great progress on the Python course! Need to complete the data structures module by next week.',
            'source_type': 'notes',
            'processed_insights': {
                'summary': 'Learning progress and goal identified',
                'urgency_level': 'low',
                'task_count': 1
            },
            'extracted_tasks': [
                {
                    'title': 'Complete Python data structures module',
                    'priority': 4,
                    'category': 'Education',
                    'deadline': '2025-01-12T23:59:00Z'
                }
            ],
            'sentiment_score': 0.8,
            'keywords': ['python', 'course', 'data', 'structures', 'module'],
            'is_processed': True
        }
    ]
    
    for entry_data in context_data:
        entry, created = ContextEntry.objects.get_or_create(
            content=entry_data['content'],
            defaults={
                'source_type': entry_data['source_type'],
                'processed_insights': entry_data['processed_insights'],
                'extracted_tasks': entry_data['extracted_tasks'],
                'sentiment_score': entry_data['sentiment_score'],
                'keywords': entry_data['keywords'],
                'is_processed': entry_data['is_processed'],
            }
        )
        
        if created:
            print(f"✅ Created context entry: {entry.preview}")

def main():
    """Main function to create all sample data."""
    print("🚀 Creating Sample Data for Smart Todo AI")
    print("=" * 50)
    
    try:
        # Create categories
        print("\n📁 Creating Categories...")
        categories = create_categories()
        
        # Create tasks
        print("\n📝 Creating Tasks...")
        create_tasks(categories)
        
        # Create context entries
        print("\n💬 Creating Context Entries...")
        create_context_entries()
        
        print("\n✅ Sample data creation complete!")
        print("\nYou can now:")
        print("1. View tasks in the web interface")
        print("2. Test AI features with the sample context")
        print("3. Explore the Django admin at /admin")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 