/**
 * API service for connecting to Django backend
 */

const API_BASE_URL = 'http://localhost:8000/api';

export interface Task {
  id: number;
  title: string;
  description: string;
  category: number | null;
  category_name?: string;
  priority_score: number;
  priority_level: string;
  deadline: string | null;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  ai_suggested: boolean;
  ai_insights: string;
  ai_enhanced_description: string;
  is_overdue: boolean;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  usage_frequency: number;
  created_at: string;
}

export interface ContextEntry {
  id: number;
  content: string;
  preview: string;
  source_type: 'whatsapp' | 'email' | 'notes' | 'calendar' | 'other';
  timestamp: string;
  processed_insights: any;
  extracted_tasks: any[];
  sentiment_score: number | null;
  keywords: string[];
  is_processed: boolean;
  processing_error: string;
}

export interface TaskStats {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  in_progress_tasks: number;
  high_priority_tasks: number;
  ai_suggested_tasks: number;
  overdue_tasks: number;
}

export interface AIEnhancement {
  priority: number;
  suggested_deadline: string | null;
  enhanced_description: string;
  suggested_categories: string[];
  insights: string;
}

class ApiService {
  private async request(endpoint: string, options: RequestInit = {}): Promise<any> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Task API methods
  async getTasks(params?: {
    status?: string;
    category?: string;
    priority?: string;
    ai_suggested?: boolean;
    search?: string;
  }): Promise<{ results: Task[]; count: number }> {
    const searchParams = new URLSearchParams();
    
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = searchParams.toString();
    const endpoint = `/tasks/${queryString ? `?${queryString}` : ''}`;
    
    return this.request(endpoint);
  }

  async getTask(id: number): Promise<Task> {
    return this.request(`/tasks/${id}/`);
  }

  async createTask(task: Partial<Task>): Promise<Task> {
    return this.request('/tasks/', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async updateTask(id: number, task: Partial<Task>): Promise<Task> {
    return this.request(`/tasks/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(task),
    });
  }

  async deleteTask(id: number): Promise<void> {
    return this.request(`/tasks/${id}/`, {
      method: 'DELETE',
    });
  }

  async getTaskStats(): Promise<TaskStats> {
    return this.request('/tasks/stats/');
  }

  async toggleTaskStatus(id: number): Promise<Task> {
    return this.request(`/tasks/${id}/toggle_status/`, {
      method: 'POST',
    });
  }

  // Category API methods
  async getCategories(): Promise<Category[]> {
    const response = await this.request('/tasks/categories/');
    return response.results || response;
  }

  // Context Entry API methods
  async getContextEntries(params?: {
    source_type?: string;
    is_processed?: boolean;
    days_back?: number;
    search?: string;
  }): Promise<{ results: ContextEntry[]; count: number }> {
    const searchParams = new URLSearchParams();
    
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = searchParams.toString();
    const endpoint = `/context/${queryString ? `?${queryString}` : ''}`;
    
    return this.request(endpoint);
  }

  async createContextEntry(entry: {
    content: string;
    source_type: string;
  }): Promise<ContextEntry> {
    return this.request('/context/', {
      method: 'POST',
      body: JSON.stringify(entry),
    });
  }

  async getContextStats(): Promise<any> {
    return this.request('/context/stats/');
  }

  async getContextInsights(): Promise<any> {
    return this.request('/context/insights/');
  }

  async reprocessContextEntry(id: number): Promise<any> {
    return this.request(`/context/${id}/reprocess/`, {
      method: 'POST',
    });
  }

  // AI Integration API methods
  async enhanceTask(task: {
    title: string;
    description: string;
    category?: string;
  }): Promise<AIEnhancement> {
    return this.request('/ai/enhance-task/', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async prioritizeTasks(taskIds: number[]): Promise<{
    prioritized_tasks: Task[];
    reasoning: string;
  }> {
    return this.request('/ai/prioritize-tasks/', {
      method: 'POST',
      body: JSON.stringify({ task_ids: taskIds }),
    });
  }

  async analyzeContext(content: string, sourceType: string): Promise<any> {
    return this.request('/ai/analyze-context/', {
      method: 'POST',
      body: JSON.stringify({
        content,
        source_type: sourceType,
      }),
    });
  }

  async getAICapabilities(): Promise<any> {
    return this.request('/ai/capabilities/');
  }
}

export const apiService = new ApiService(); 