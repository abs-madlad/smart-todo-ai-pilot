
import { useState } from 'react';
import { X, Brain, Calendar, Tag, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';

interface CreateTaskModalProps {
  onClose: () => void;
}

const CreateTaskModal = ({ onClose }: CreateTaskModalProps) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('');
  const [deadline, setDeadline] = useState('');
  const [showAiSuggestions, setShowAiSuggestions] = useState(false);

  // Mock AI suggestions
  const aiSuggestions = {
    priority: 7,
    suggestedDeadline: '2025-01-10',
    enhancedDescription: 'Complete project presentation with quarterly metrics, budget analysis, and future roadmap for the Q4 review meeting. Include performance charts and stakeholder feedback.',
    suggestedCategories: ['Work', 'Presentation', 'Quarterly Review'],
    insights: 'Based on your calendar, this should be high priority. Similar tasks usually take 2-3 days to complete properly.'
  };

  const handleAiEnhance = () => {
    setShowAiSuggestions(true);
    // In a real app, this would call the AI API
    console.log('AI enhancement requested for:', { title, description, category });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // In a real app, this would submit to the backend
    console.log('Task created:', {
      title,
      description,
      category,
      deadline,
      aiEnhanced: showAiSuggestions
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200">
          <h2 className="text-xl font-semibold text-slate-900">Create New Task</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Task Title *
            </label>
            <Input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter task title..."
              required
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Description
            </label>
            <Textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe your task..."
              rows={3}
            />
          </div>

          {/* AI Enhancement Section */}
          {title && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-blue-600" />
                  <span className="font-medium text-blue-900">AI Enhancement</span>
                </div>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={handleAiEnhance}
                  className="border-blue-300 text-blue-700 hover:bg-blue-100"
                >
                  Enhance Task
                </Button>
              </div>
              
              {showAiSuggestions && (
                <div className="space-y-3">
                  <div className="text-sm text-blue-800">
                    <p className="font-medium mb-1">AI Insights:</p>
                    <p>{aiSuggestions.insights}</p>
                  </div>
                  
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                      Priority: {aiSuggestions.priority}/10
                    </Badge>
                    <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                      Suggested: {new Date(aiSuggestions.suggestedDeadline).toLocaleDateString()}
                    </Badge>
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <Tag className="inline h-4 w-4 mr-1" />
                Category
              </label>
              <Input
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="e.g., Work, Personal..."
              />
              {showAiSuggestions && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {aiSuggestions.suggestedCategories.map((cat, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => setCategory(cat)}
                      className="text-xs px-2 py-1 bg-slate-100 text-slate-700 rounded hover:bg-slate-200 transition-colors"
                    >
                      {cat}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Deadline */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <Calendar className="inline h-4 w-4 mr-1" />
                Deadline
              </label>
              <Input
                type="date"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
              />
              {showAiSuggestions && (
                <button
                  type="button"
                  onClick={() => setDeadline(aiSuggestions.suggestedDeadline)}
                  className="mt-1 text-xs text-blue-600 hover:text-blue-800"
                >
                  Use AI suggestion: {new Date(aiSuggestions.suggestedDeadline).toLocaleDateString()}
                </button>
              )}
            </div>
          </div>

          {/* Enhanced Description */}
          {showAiSuggestions && (
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                AI Enhanced Description
              </label>
              <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                <p className="text-sm text-green-800">{aiSuggestions.enhancedDescription}</p>
                <button
                  type="button"
                  onClick={() => setDescription(aiSuggestions.enhancedDescription)}
                  className="mt-2 text-xs text-green-600 hover:text-green-800"
                >
                  Use this enhanced description
                </button>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-200">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700"
            >
              Create Task
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateTaskModal;
