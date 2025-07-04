
import { useState } from 'react';
import { Plus, Brain, Calendar, Filter, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import TaskCard from '@/components/TaskCard';
import CreateTaskModal from '@/components/CreateTaskModal';
import ContextInput from '@/components/ContextInput';
import StatsOverview from '@/components/StatsOverview';

const Index = () => {
  const [activeTab, setActiveTab] = useState('tasks');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');

  // Mock data for demonstration
  const mockTasks = [
    {
      id: 1,
      title: "Complete project presentation",
      description: "Prepare slides for quarterly review meeting",
      category: "Work",
      priority: 9,
      deadline: "2025-01-08",
      status: "pending",
      aiSuggested: true,
      aiInsights: "High priority based on upcoming deadline and email context"
    },
    {
      id: 2,
      title: "Buy groceries",
      description: "Weekly grocery shopping for the family",
      category: "Personal",
      priority: 5,
      deadline: "2025-01-06",
      status: "pending",
      aiSuggested: false
    },
    {
      id: 3,
      title: "Schedule dentist appointment",
      description: "Annual dental checkup",
      category: "Health",
      priority: 6,
      deadline: "2025-01-15",
      status: "completed",
      aiSuggested: true,
      aiInsights: "Suggested based on calendar analysis"
    }
  ];

  const filteredTasks = mockTasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         task.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = selectedFilter === 'all' || 
                         (selectedFilter === 'pending' && task.status === 'pending') ||
                         (selectedFilter === 'completed' && task.status === 'completed') ||
                         (selectedFilter === 'ai-suggested' && task.aiSuggested);
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-slate-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Brain className="h-8 w-8 text-blue-600" />
                <h1 className="text-2xl font-bold text-slate-900">Smart Todo</h1>
              </div>
              <nav className="hidden md:flex space-x-8">
                <button
                  onClick={() => setActiveTab('tasks')}
                  className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                    activeTab === 'tasks'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  Tasks
                </button>
                <button
                  onClick={() => setActiveTab('context')}
                  className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                    activeTab === 'context'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  Daily Context
                </button>
              </nav>
            </div>
            <Button
              onClick={() => setShowCreateModal(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Task
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'tasks' && (
          <div className="space-y-8">
            {/* Stats Overview */}
            <StatsOverview tasks={mockTasks} />

            {/* Search and Filter */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                  <Input
                    placeholder="Search tasks..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <div className="flex items-center space-x-2">
                  <Filter className="h-4 w-4 text-slate-400" />
                  <select
                    value={selectedFilter}
                    onChange={(e) => setSelectedFilter(e.target.value)}
                    className="px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Tasks</option>
                    <option value="pending">Pending</option>
                    <option value="completed">Completed</option>
                    <option value="ai-suggested">AI Suggested</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Tasks Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredTasks.map((task) => (
                <TaskCard key={task.id} task={task} />
              ))}
            </div>

            {filteredTasks.length === 0 && (
              <div className="text-center py-12">
                <Calendar className="mx-auto h-12 w-12 text-slate-400" />
                <h3 className="mt-2 text-sm font-medium text-slate-900">No tasks found</h3>
                <p className="mt-1 text-sm text-slate-500">
                  {searchQuery || selectedFilter !== 'all'
                    ? 'Try adjusting your search or filter.'
                    : 'Get started by adding your first task.'}
                </p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'context' && <ContextInput />}
      </main>

      {/* Create Task Modal */}
      {showCreateModal && (
        <CreateTaskModal onClose={() => setShowCreateModal(false)} />
      )}
    </div>
  );
};

export default Index;
