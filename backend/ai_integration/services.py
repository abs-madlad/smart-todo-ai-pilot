"""
AI Integration Services for Smart Todo Application.
Supports OpenAI, Anthropic Claude, and LM Studio.
"""

import json
import re
import requests
from datetime import datetime, timedelta
from django.conf import settings
from typing import Dict, List, Optional, Any


class AIService:
    """Main AI service class that handles different AI providers."""
    
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.anthropic_key = settings.ANTHROPIC_API_KEY
        self.lm_studio_url = settings.LM_STUDIO_BASE_URL
        
    def analyze_context(self, content: str, source_type: str) -> Dict[str, Any]:
        """
        Analyze context content and extract insights, tasks, and metadata.
        
        Args:
            content: The text content to analyze
            source_type: Type of source (whatsapp, email, notes, etc.)
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Try different AI providers in order of preference
            if self.lm_studio_url:
                return self._analyze_with_lm_studio(content, source_type)
            elif self.anthropic_key:
                return self._analyze_with_claude(content, source_type)
            elif self.openai_key:
                return self._analyze_with_openai(content, source_type)
            else:
                # Fallback to rule-based analysis
                return self._analyze_with_rules(content, source_type)
                
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._analyze_with_rules(content, source_type)
    
    def enhance_task(self, title: str, description: str, category: str = None) -> Dict[str, Any]:
        """
        Enhance a task with AI-powered suggestions.
        
        Args:
            title: Task title
            description: Task description
            category: Optional category
            
        Returns:
            Dictionary with enhanced task data
        """
        try:
            if self.lm_studio_url:
                return self._enhance_task_lm_studio(title, description, category)
            elif self.anthropic_key:
                return self._enhance_task_claude(title, description, category)
            elif self.openai_key:
                return self._enhance_task_openai(title, description, category)
            else:
                return self._enhance_task_rules(title, description, category)
                
        except Exception as e:
            print(f"Task enhancement failed: {e}")
            return self._enhance_task_rules(title, description, category)
    
    def prioritize_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """
        Prioritize tasks based on AI analysis.
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            List of tasks with updated priority scores
        """
        try:
            if self.lm_studio_url:
                return self._prioritize_with_lm_studio(tasks)
            elif self.anthropic_key:
                return self._prioritize_with_claude(tasks)
            elif self.openai_key:
                return self._prioritize_with_openai(tasks)
            else:
                return self._prioritize_with_rules(tasks)
                
        except Exception as e:
            print(f"Task prioritization failed: {e}")
            return self._prioritize_with_rules(tasks)
    
    # LM Studio Implementation
    def _analyze_with_lm_studio(self, content: str, source_type: str) -> Dict[str, Any]:
        """Analyze content using LM Studio local model."""
        prompt = self._build_context_analysis_prompt(content, source_type)
        
        response = requests.post(
            f"{self.lm_studio_url}/v1/chat/completions",
            json={
                "model": "local-model",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return self._parse_analysis_response(ai_response)
        else:
            raise Exception(f"LM Studio API error: {response.status_code}")
    
    def _enhance_task_lm_studio(self, title: str, description: str, category: str) -> Dict[str, Any]:
        """Enhance task using LM Studio."""
        prompt = self._build_task_enhancement_prompt(title, description, category)
        
        response = requests.post(
            f"{self.lm_studio_url}/v1/chat/completions",
            json={
                "model": "local-model",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return self._parse_enhancement_response(ai_response)
        else:
            raise Exception(f"LM Studio API error: {response.status_code}")
    
    def _prioritize_with_lm_studio(self, tasks: List[Dict]) -> List[Dict]:
        """Prioritize tasks using LM Studio."""
        prompt = self._build_prioritization_prompt(tasks)
        
        response = requests.post(
            f"{self.lm_studio_url}/v1/chat/completions",
            json={
                "model": "local-model",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5,
                "max_tokens": 800
            },
            timeout=25
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return self._parse_prioritization_response(ai_response, tasks)
        else:
            raise Exception(f"LM Studio API error: {response.status_code}")
    
    # OpenAI Implementation
    def _analyze_with_openai(self, content: str, source_type: str) -> Dict[str, Any]:
        """Analyze content using OpenAI API."""
        import openai
        
        openai.api_key = self.openai_key
        prompt = self._build_context_analysis_prompt(content, source_type)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        ai_response = response.choices[0].message.content
        return self._parse_analysis_response(ai_response)
    
    def _enhance_task_openai(self, title: str, description: str, category: str) -> Dict[str, Any]:
        """Enhance task using OpenAI."""
        import openai
        
        openai.api_key = self.openai_key
        prompt = self._build_task_enhancement_prompt(title, description, category)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        return self._parse_enhancement_response(ai_response)
    
    def _prioritize_with_openai(self, tasks: List[Dict]) -> List[Dict]:
        """Prioritize tasks using OpenAI."""
        import openai
        
        openai.api_key = self.openai_key
        prompt = self._build_prioritization_prompt(tasks)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=800
        )
        
        ai_response = response.choices[0].message.content
        return self._parse_prioritization_response(ai_response, tasks)
    
    # Claude Implementation
    def _analyze_with_claude(self, content: str, source_type: str) -> Dict[str, Any]:
        """Analyze content using Anthropic Claude."""
        import anthropic
        
        client = anthropic.Anthropic(api_key=self.anthropic_key)
        prompt = self._build_context_analysis_prompt(content, source_type)
        
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        ai_response = response.content[0].text
        return self._parse_analysis_response(ai_response)
    
    def _enhance_task_claude(self, title: str, description: str, category: str) -> Dict[str, Any]:
        """Enhance task using Claude."""
        import anthropic
        
        client = anthropic.Anthropic(api_key=self.anthropic_key)
        prompt = self._build_task_enhancement_prompt(title, description, category)
        
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        ai_response = response.content[0].text
        return self._parse_enhancement_response(ai_response)
    
    def _prioritize_with_claude(self, tasks: List[Dict]) -> List[Dict]:
        """Prioritize tasks using Claude."""
        import anthropic
        
        client = anthropic.Anthropic(api_key=self.anthropic_key)
        prompt = self._build_prioritization_prompt(tasks)
        
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        
        ai_response = response.content[0].text
        return self._parse_prioritization_response(ai_response, tasks)
    
    # Rule-based fallback implementations
    def _analyze_with_rules(self, content: str, source_type: str) -> Dict[str, Any]:
        """Fallback rule-based context analysis."""
        # Extract keywords
        keywords = self._extract_keywords_simple(content)
        
        # Detect tasks using patterns
        task_patterns = [
            r'need to (.+?)(?:\.|$)',
            r'should (.+?)(?:\.|$)',
            r'must (.+?)(?:\.|$)',
            r'have to (.+?)(?:\.|$)',
            r'remember to (.+?)(?:\.|$)',
            r'don\'t forget to (.+?)(?:\.|$)',
        ]
        
        extracted_tasks = []
        for pattern in task_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                task_text = match.group(1).strip()
                if len(task_text) > 5:  # Minimum length
                    priority = self._estimate_priority_rules(task_text, content)
                    extracted_tasks.append({
                        'title': task_text.capitalize(),
                        'description': f'Extracted from {source_type}',
                        'priority': priority,
                        'category': self._guess_category_rules(task_text)
                    })
        
        # Sentiment analysis (simple)
        sentiment_score = self._analyze_sentiment_simple(content)
        
        return {
            'insights': {
                'summary': f'Analyzed {source_type} content with {len(extracted_tasks)} potential tasks',
                'task_count': len(extracted_tasks),
                'sentiment': 'positive' if sentiment_score > 0 else 'negative' if sentiment_score < 0 else 'neutral'
            },
            'extracted_tasks': extracted_tasks,
            'sentiment_score': sentiment_score,
            'keywords': keywords
        }
    
    def _enhance_task_rules(self, title: str, description: str, category: str) -> Dict[str, Any]:
        """Fallback rule-based task enhancement."""
        # Estimate priority based on keywords
        priority = self._estimate_priority_rules(title + ' ' + description)
        
        # Suggest deadline based on urgency keywords
        deadline = self._suggest_deadline_rules(title + ' ' + description)
        
        # Enhanced description
        enhanced_desc = description
        if not enhanced_desc:
            enhanced_desc = f"Task: {title}"
        
        return {
            'priority': priority,
            'suggested_deadline': deadline,
            'enhanced_description': enhanced_desc,
            'suggested_categories': [category] if category else ['General'],
            'insights': f'Priority {priority}/10 based on content analysis'
        }
    
    def _prioritize_with_rules(self, tasks: List[Dict]) -> List[Dict]:
        """Fallback rule-based task prioritization."""
        for task in tasks:
            content = f"{task.get('title', '')} {task.get('description', '')}"
            task['priority_score'] = self._estimate_priority_rules(content)
        
        return sorted(tasks, key=lambda x: x.get('priority_score', 5), reverse=True)
    
    # Helper methods
    def _build_context_analysis_prompt(self, content: str, source_type: str) -> str:
        """Build prompt for context analysis."""
        return f"""
        Analyze the following {source_type} content and extract actionable insights:

        Content: "{content}"

        Please provide a JSON response with:
        1. insights: {{summary, task_count, urgency_level}}
        2. extracted_tasks: [{{title, description, priority (1-10), category, deadline}}]
        3. sentiment_score: float between -1 and 1
        4. keywords: list of relevant keywords

        Focus on identifying tasks, deadlines, and priorities. Be practical and actionable.
        """
    
    def _build_task_enhancement_prompt(self, title: str, description: str, category: str) -> str:
        """Build prompt for task enhancement."""
        return f"""
        Enhance this task with AI-powered suggestions:

        Title: {title}
        Description: {description}
        Category: {category or 'Unknown'}

        Please provide a JSON response with:
        1. priority: integer 1-10 (based on urgency and importance)
        2. suggested_deadline: ISO date string (realistic estimate)
        3. enhanced_description: improved, more detailed description
        4. suggested_categories: list of relevant categories
        5. insights: explanation of priority and recommendations

        Be practical and helpful in your suggestions.
        """
    
    def _build_prioritization_prompt(self, tasks: List[Dict]) -> str:
        """Build prompt for task prioritization."""
        task_list = "\n".join([
            f"{i+1}. {task.get('title', 'Untitled')} - {task.get('description', '')}"
            for i, task in enumerate(tasks)
        ])
        
        return f"""
        Prioritize these tasks based on urgency and importance:

        {task_list}

        Please provide a JSON response with:
        - prioritized_tasks: array of task indices (0-based) in priority order
        - priority_scores: array of scores 1-10 for each task
        - reasoning: explanation of prioritization logic

        Consider deadlines, complexity, and impact when prioritizing.
        """
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for context analysis."""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback parsing
        return {
            'insights': {'summary': 'AI analysis completed'},
            'extracted_tasks': [],
            'sentiment_score': 0.0,
            'keywords': []
        }
    
    def _parse_enhancement_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for task enhancement."""
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {
            'priority': 5,
            'suggested_deadline': None,
            'enhanced_description': '',
            'suggested_categories': [],
            'insights': 'Enhancement completed'
        }
    
    def _parse_prioritization_response(self, response: str, tasks: List[Dict]) -> List[Dict]:
        """Parse AI response for task prioritization."""
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                priority_scores = data.get('priority_scores', [])
                
                for i, task in enumerate(tasks):
                    if i < len(priority_scores):
                        task['priority_score'] = priority_scores[i]
                
                return tasks
        except:
            pass
        
        return tasks
    
    def _estimate_priority_rules(self, content: str, context: str = '') -> int:
        """Estimate priority using rule-based approach."""
        content_lower = content.lower()
        
        # High priority keywords
        high_priority = ['urgent', 'asap', 'immediately', 'critical', 'important', 'deadline', 'due']
        # Medium priority keywords
        medium_priority = ['soon', 'today', 'tomorrow', 'this week', 'meeting', 'call']
        # Low priority keywords
        low_priority = ['later', 'eventually', 'when possible', 'someday']
        
        priority = 5  # Default
        
        for keyword in high_priority:
            if keyword in content_lower:
                priority = max(priority, 8)
        
        for keyword in medium_priority:
            if keyword in content_lower:
                priority = max(priority, 6)
        
        for keyword in low_priority:
            if keyword in content_lower:
                priority = min(priority, 3)
        
        return priority
    
    def _suggest_deadline_rules(self, content: str) -> Optional[str]:
        """Suggest deadline using rule-based approach."""
        content_lower = content.lower()
        
        # Look for time indicators
        if any(word in content_lower for word in ['today', 'asap', 'immediately']):
            return (datetime.now() + timedelta(days=1)).isoformat()
        elif any(word in content_lower for word in ['tomorrow', 'next day']):
            return (datetime.now() + timedelta(days=2)).isoformat()
        elif any(word in content_lower for word in ['this week', 'week']):
            return (datetime.now() + timedelta(days=7)).isoformat()
        elif any(word in content_lower for word in ['next week']):
            return (datetime.now() + timedelta(days=14)).isoformat()
        elif any(word in content_lower for word in ['month', 'monthly']):
            return (datetime.now() + timedelta(days=30)).isoformat()
        
        return None
    
    def _guess_category_rules(self, content: str) -> str:
        """Guess category using rule-based approach."""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['work', 'office', 'meeting', 'project', 'client']):
            return 'Work'
        elif any(word in content_lower for word in ['doctor', 'health', 'gym', 'exercise', 'medical']):
            return 'Health'
        elif any(word in content_lower for word in ['buy', 'shop', 'grocery', 'store', 'purchase']):
            return 'Shopping'
        elif any(word in content_lower for word in ['family', 'home', 'house', 'personal']):
            return 'Personal'
        elif any(word in content_lower for word in ['learn', 'study', 'course', 'education']):
            return 'Education'
        else:
            return 'General'
    
    def _extract_keywords_simple(self, text: str) -> List[str]:
        """Simple keyword extraction."""
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in stop_words]
        
        # Return most frequent keywords
        from collections import Counter
        word_freq = Counter(keywords)
        return [word for word, count in word_freq.most_common(10)]
    
    def _analyze_sentiment_simple(self, text: str) -> float:
        """Simple sentiment analysis."""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy', 'excited']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated', 'annoyed', 'upset']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count + negative_count == 0:
            return 0.0
        
        return (positive_count - negative_count) / (positive_count + negative_count) 