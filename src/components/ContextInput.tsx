
import { useState } from 'react';
import { MessageCircle, Mail, FileText, Brain, Plus, Calendar } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';

const ContextInput = () => {
  const [activeTab, setActiveTab] = useState('whatsapp');
  const [contextText, setContextText] = useState('');
  const [showAnalysis, setShowAnalysis] = useState(false);

  // Mock context data
  const mockContextHistory = [
    {
      id: 1,
      type: 'whatsapp',
      content: 'Meeting with client tomorrow at 3 PM. Need to prepare the quarterly report.',
      timestamp: '2025-01-04 14:30',
      insights: ['High priority task detected', 'Deadline: Tomorrow 3 PM', 'Context: Client meeting']
    },
    {
      id: 2,
      type: 'email',
      content: 'Reminder: Annual performance reviews are due by January 15th.',
      timestamp: '2025-01-04 09:15',
      insights: ['Deadline detected: Jan 15', 'Task type: Performance review', 'Category: HR/Work']
    },
    {
      id: 3,
      type: 'notes',
      content: 'Grocery list: milk, bread, eggs. Also need to book dentist appointment.',
      timestamp: '2025-01-03 18:45',
      insights: ['Personal tasks identified', 'Categories: Shopping, Health', 'Multiple actions needed']
    }
  ];

  const contextTypes = [
    { id: 'whatsapp', label: 'WhatsApp', icon: MessageCircle, color: 'text-green-600' },
    { id: 'email', label: 'Email', icon: Mail, color: 'text-blue-600' },
    { id: 'notes', label: 'Notes', icon: FileText, color: 'text-purple-600' }
  ];

  const handleAnalyze = () => {
    if (!contextText.trim()) return;
    
    setShowAnalysis(true);
    // In a real app, this would call the AI API for context analysis
    console.log('Analyzing context:', { type: activeTab, content: contextText });
  };

  const handleSave = () => {
    if (!contextText.trim()) return;
    
    // In a real app, this would save to the backend
    console.log('Saving context:', { type: activeTab, content: contextText });
    setContextText('');
    setShowAnalysis(false);
  };

  // Mock AI analysis results
  const analysisResults = {
    extractedTasks: [
      { title: 'Prepare quarterly report', priority: 9, category: 'Work', deadline: '2025-01-05' },
      { title: 'Client meeting preparation', priority: 8, category: 'Work', deadline: '2025-01-05' }
    ],
    insights: [
      'High urgency detected based on "tomorrow" reference',
      'Client-related context suggests work priority',
      'Multiple related tasks identified'
    ],
    suggestedActions: [
      'Create high-priority task for quarterly report',
      'Block calendar time for meeting preparation',
      'Set reminder for client meeting'
    ]
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="flex items-center space-x-3 mb-4">
          <Brain className="h-6 w-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-slate-900">Daily Context Analysis</h2>
        </div>
        <p className="text-slate-600">
          Add your daily context from messages, emails, and notes. Our AI will analyze them to suggest relevant tasks and priorities.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Context Input */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Add Context</h3>
          
          {/* Context Type Tabs */}
          <div className="flex space-x-1 mb-4 bg-slate-100 rounded-lg p-1">
            {contextTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => setActiveTab(type.id)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === type.id
                    ? 'bg-white text-slate-900 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <type.icon className={`h-4 w-4 ${type.color}`} />
                <span>{type.label}</span>
              </button>
            ))}
          </div>

          {/* Context Input Area */}
          <div className="space-y-4">
            <Textarea
              value={contextText}
              onChange={(e) => setContextText(e.target.value)}
              placeholder={`Paste your ${contextTypes.find(t => t.id === activeTab)?.label.toLowerCase()} content here...`}
              rows={6}
            />
            
            <div className="flex space-x-3">
              <Button
                onClick={handleAnalyze}
                disabled={!contextText.trim()}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Brain className="h-4 w-4 mr-2" />
                Analyze Context
              </Button>
              <Button
                variant="outline"
                onClick={handleSave}
                disabled={!contextText.trim()}
              >
                <Plus className="h-4 w-4 mr-2" />
                Save Context
              </Button>
            </div>
          </div>

          {/* AI Analysis Results */}
          {showAnalysis && (
            <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-medium text-blue-900 mb-3">AI Analysis Results</h4>
              
              {/* Extracted Tasks */}
              <div className="mb-4">
                <h5 className="text-sm font-medium text-blue-800 mb-2">Suggested Tasks:</h5>
                <div className="space-y-2">
                  {analysisResults.extractedTasks.map((task, index) => (
                    <div key={index} className="bg-white rounded-lg p-3 border border-blue-200">
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-slate-900">{task.title}</span>
                        <Badge variant="secondary" className="text-xs">
                          P{task.priority}
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-slate-600">
                        <span>{task.category}</span>
                        <span className="flex items-center">
                          <Calendar className="h-3 w-3 mr-1" />
                          {new Date(task.deadline).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Insights */}
              <div className="mb-4">
                <h5 className="text-sm font-medium text-blue-800 mb-2">Insights:</h5>
                <ul className="text-sm text-blue-700 space-y-1">
                  {analysisResults.insights.map((insight, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <span className="text-blue-500">•</span>
                      <span>{insight}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Action Buttons */}
              <div className="flex space-x-2">
                <Button size="sm" className="bg-green-600 hover:bg-green-700 text-xs">
                  Create All Tasks
                </Button>
                <Button variant="outline" size="sm" className="text-xs">
                  Review & Edit
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Context History */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Recent Context</h3>
          
          <div className="space-y-4">
            {mockContextHistory.map((item) => {
              const contextType = contextTypes.find(t => t.id === item.type);
              return (
                <div key={item.id} className="border border-slate-200 rounded-lg p-4">
                  <div className="flex items-center space-x-2 mb-2">
                    {contextType && <contextType.icon className={`h-4 w-4 ${contextType.color}`} />}
                    <span className="text-sm font-medium text-slate-900">{contextType?.label}</span>
                    <span className="text-xs text-slate-500">{item.timestamp}</span>
                  </div>
                  
                  <p className="text-sm text-slate-700 mb-3">{item.content}</p>
                  
                  <div className="space-y-1">
                    <h6 className="text-xs font-medium text-slate-600">AI Insights:</h6>
                    {item.insights.map((insight, index) => (
                      <Badge key={index} variant="secondary" className="text-xs mr-2 mb-1">
                        {insight}
                      </Badge>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContextInput;
