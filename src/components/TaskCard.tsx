
import { useState } from 'react';
import { Calendar, Tag, Brain, CheckCircle2, Circle, Clock, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface Task {
  id: number;
  title: string;
  description: string;
  category: string;
  priority: number;
  deadline: string;
  status: 'pending' | 'completed';
  aiSuggested?: boolean;
  aiInsights?: string;
}

interface TaskCardProps {
  task: Task;
}

const TaskCard = ({ task }: TaskCardProps) => {
  const [isCompleted, setIsCompleted] = useState(task.status === 'completed');

  const toggleComplete = () => {
    setIsCompleted(!isCompleted);
  };

  const getPriorityColor = (priority: number) => {
    if (priority >= 8) return 'text-red-600 bg-red-50 border-red-200';
    if (priority >= 6) return 'text-amber-600 bg-amber-50 border-amber-200';
    return 'text-green-600 bg-green-50 border-green-200';
  };

  const getPriorityIcon = (priority: number) => {
    if (priority >= 8) return <AlertTriangle className="h-4 w-4" />;
    if (priority >= 6) return <Clock className="h-4 w-4" />;
    return <Circle className="h-4 w-4" />;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = date.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Tomorrow';
    if (diffDays < 0) return `${Math.abs(diffDays)} days overdue`;
    return `${diffDays} days left`;
  };

  const isOverdue = new Date(task.deadline) < new Date();

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow ${
      isCompleted ? 'opacity-75' : ''
    }`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <button
            onClick={toggleComplete}
            className="text-slate-400 hover:text-blue-600 transition-colors"
          >
            {isCompleted ? (
              <CheckCircle2 className="h-5 w-5 text-green-600" />
            ) : (
              <Circle className="h-5 w-5" />
            )}
          </button>
          <div className="flex-1">
            <h3 className={`font-semibold text-slate-900 ${isCompleted ? 'line-through' : ''}`}>
              {task.title}
            </h3>
          </div>
        </div>
        
        {task.aiSuggested && (
          <Badge variant="secondary" className="bg-blue-50 text-blue-700 border-blue-200">
            <Brain className="h-3 w-3 mr-1" />
            AI
          </Badge>
        )}
      </div>

      {/* Description */}
      <p className="text-slate-600 text-sm mb-4 line-clamp-2">{task.description}</p>

      {/* AI Insights */}
      {task.aiInsights && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
          <div className="flex items-start space-x-2">
            <Brain className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
            <p className="text-blue-800 text-xs">{task.aiInsights}</p>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {/* Category */}
          <div className="flex items-center space-x-1 text-slate-500">
            <Tag className="h-4 w-4" />
            <span className="text-xs">{task.category}</span>
          </div>

          {/* Deadline */}
          <div className={`flex items-center space-x-1 ${
            isOverdue ? 'text-red-600' : 'text-slate-500'
          }`}>
            <Calendar className="h-4 w-4" />
            <span className="text-xs">{formatDate(task.deadline)}</span>
          </div>
        </div>

        {/* Priority */}
        <div className={`flex items-center space-x-1 px-2 py-1 rounded-full border text-xs font-medium ${
          getPriorityColor(task.priority)
        }`}>
          {getPriorityIcon(task.priority)}
          <span>P{task.priority}</span>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
