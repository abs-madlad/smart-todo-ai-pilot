# Smart Todo List with AI Integration

A full-stack web application that combines intelligent task management with AI-powered features for enhanced productivity. The system analyzes daily context (messages, emails, notes) to provide smart task suggestions, prioritization, and deadline recommendations.

## 🚀 Features

### Core Functionality
- **Task Management**: Create, edit, delete, and organize tasks with categories
- **AI-Powered Prioritization**: Automatic task priority scoring based on context analysis
- **Smart Deadline Suggestions**: AI-recommended deadlines based on task complexity and urgency
- **Context Analysis**: Process daily context from WhatsApp, emails, and notes
- **Intelligent Categorization**: Auto-suggest task categories and tags
- **Advanced Search & Filtering**: Filter by status, priority, category, and AI suggestions

### AI Integration
- **Multiple AI Providers**: Support for OpenAI, Anthropic Claude, and LM Studio
- **Context Processing**: Analyze daily context to understand user's schedule and priorities
- **Task Enhancement**: Improve task descriptions with context-aware details
- **Sentiment Analysis**: Analyze emotional context from input sources
- **Keyword Extraction**: Identify relevant keywords from context entries
- **Auto-Task Creation**: Automatically create high-priority tasks from context analysis

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: PostgreSQL (Supabase)
- **AI Integration**: OpenAI GPT, Anthropic Claude, LM Studio
- **Authentication**: Django built-in authentication
- **API**: RESTful API with comprehensive endpoints

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **Build Tool**: Vite
- **State Management**: React Query for server state
- **UI Components**: Modern, responsive design with dark mode support

### AI Providers
- **OpenAI**: GPT-3.5-turbo for context analysis and task enhancement
- **Anthropic Claude**: Claude-3-sonnet for advanced reasoning
- **LM Studio**: Local LLM hosting for privacy-focused AI processing
- **Fallback**: Rule-based processing when AI providers are unavailable

## 📦 Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL (or Supabase account)
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-todo-ai-pilot
   ```

2. **Set up Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   # Django Configuration
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   
   # Database Configuration (Supabase)
   SUPABASE_DB_NAME=postgres
   SUPABASE_DB_USER=postgres
   SUPABASE_DB_PASSWORD=your-supabase-password
   SUPABASE_DB_HOST=your-supabase-host
   SUPABASE_DB_PORT=5432
   
   # AI Integration (choose one or more)
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   LM_STUDIO_BASE_URL=http://localhost:1234
   ```

5. **Database Migration**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Backend Server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to project root**
   ```bash
   cd ..  # From backend directory
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

The application will be available at:
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin

## 🔧 AI Integration Setup

### Option 1: OpenAI API
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env`: `OPENAI_API_KEY=your-key-here`

### Option 2: Anthropic Claude
1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Add to `.env`: `ANTHROPIC_API_KEY=your-key-here`

### Option 3: LM Studio (Recommended)
1. Download [LM Studio](https://lmstudio.ai/)
2. Install a model (e.g., Llama 2, Mistral)
3. Start local server on port 1234
4. Add to `.env`: `LM_STUDIO_BASE_URL=http://localhost:1234`

## 📚 API Documentation

### Task Endpoints
- `GET /api/tasks/` - List all tasks with filtering
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get specific task
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `GET /api/tasks/stats/` - Get task statistics
- `POST /api/tasks/{id}/toggle_status/` - Toggle task completion

### Context Endpoints
- `GET /api/context/` - List context entries
- `POST /api/context/` - Create context entry
- `GET /api/context/stats/` - Get context statistics
- `GET /api/context/insights/` - Get aggregated insights
- `POST /api/context/{id}/reprocess/` - Reprocess with AI

### AI Integration Endpoints
- `POST /api/ai/enhance-task/` - Enhance task with AI
- `POST /api/ai/prioritize-tasks/` - Prioritize tasks using AI
- `POST /api/ai/analyze-context/` - Analyze context content
- `GET /api/ai/capabilities/` - Get AI provider status

### Category Endpoints
- `GET /api/tasks/categories/` - List all categories

## 📊 Database Schema

### Tasks Table
```sql
- id: Primary Key
- title: VARCHAR(255)
- description: TEXT
- category: ForeignKey to Category
- priority_score: INTEGER (1-10)
- deadline: DATETIME
- status: VARCHAR(20) [pending, in_progress, completed, cancelled]
- ai_suggested: BOOLEAN
- ai_insights: TEXT
- ai_enhanced_description: TEXT
- created_at: DATETIME
- updated_at: DATETIME
```

### Context Entries Table
```sql
- id: Primary Key
- content: TEXT
- source_type: VARCHAR(20) [whatsapp, email, notes, calendar, other]
- timestamp: DATETIME
- processed_insights: JSON
- extracted_tasks: JSON
- sentiment_score: FLOAT
- keywords: JSON
- is_processed: BOOLEAN
- processing_error: TEXT
```

### Categories Table
```sql
- id: Primary Key
- name: VARCHAR(100)
- usage_frequency: INTEGER
- created_at: DATETIME
```

## 🧪 Sample Data & Testing

### Sample Tasks
```json
{
  "title": "Complete project presentation",
  "description": "Prepare slides for quarterly review meeting",
  "category": "Work",
  "priority_score": 9,
  "deadline": "2025-01-08T15:00:00Z",
  "ai_suggested": true,
  "ai_insights": "High priority based on upcoming deadline and email context"
}
```

### Sample Context Entry
```json
{
  "content": "Meeting with client tomorrow at 3 PM. Need to prepare the quarterly report.",
  "source_type": "whatsapp",
  "processed_insights": {
    "summary": "Client meeting detected with preparation task",
    "urgency_level": "high",
    "task_count": 2
  },
  "extracted_tasks": [
    {
      "title": "Prepare quarterly report",
      "priority": 9,
      "category": "Work",
      "deadline": "2025-01-05T15:00:00Z"
    }
  ],
  "sentiment_score": 0.1,
  "keywords": ["meeting", "client", "quarterly", "report"]
}
```

## 🎯 AI Features Demo

### Context Analysis Example
**Input**: "Don't forget to buy groceries tomorrow and call the dentist to schedule an appointment this week"

**AI Analysis Output**:
```json
{
  "insights": {
    "summary": "Personal tasks identified with time constraints",
    "task_count": 2,
    "urgency_level": "medium"
  },
  "extracted_tasks": [
    {
      "title": "Buy groceries",
      "priority": 6,
      "category": "Shopping",
      "deadline": "2025-01-06"
    },
    {
      "title": "Call dentist for appointment",
      "priority": 5,
      "category": "Health",
      "deadline": "2025-01-10"
    }
  ],
  "sentiment_score": 0.0,
  "keywords": ["groceries", "dentist", "appointment", "schedule"]
}
```

### Task Enhancement Example
**Input**: "Finish report"

**AI Enhancement Output**:
```json
{
  "priority": 7,
  "suggested_deadline": "2025-01-08T17:00:00Z",
  "enhanced_description": "Complete the comprehensive report including data analysis, recommendations, and executive summary for stakeholder review",
  "suggested_categories": ["Work", "Documentation", "Analysis"],
  "insights": "Priority 7/10 based on professional context and typical report completion timeframes"
}
```

## 🔍 Advanced Features

### Smart Prioritization Algorithm
The AI considers multiple factors:
- **Urgency keywords**: "urgent", "asap", "deadline"
- **Context analysis**: Meeting references, time constraints
- **Category importance**: Work > Health > Personal
- **Deadline proximity**: Closer deadlines get higher priority
- **Task complexity**: Estimated completion time

### Sentiment Analysis
- **Positive sentiment**: Tasks from positive contexts get balanced priority
- **Negative sentiment**: May indicate stress, potentially increasing priority
- **Neutral sentiment**: Standard priority calculation

### Auto-Task Creation
- High-priority tasks (score ≥ 8) are automatically created from context
- Prevents important tasks from being missed
- Includes AI-generated insights explaining the creation reason

## 🚀 Deployment

### Backend Deployment (Django)
1. Set up production database (Supabase recommended)
2. Configure environment variables
3. Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic`
5. Deploy to platform (Heroku, DigitalOcean, AWS)

### Frontend Deployment
1. Build production version: `npm run build`
2. Deploy to static hosting (Vercel, Netlify, S3)
3. Configure API base URL for production

## 🛡 Security & Privacy

- **Data Encryption**: All API communications use HTTPS
- **Local AI Option**: LM Studio provides complete data privacy
- **No Data Persistence**: AI providers don't store processed content
- **Environment Variables**: Sensitive keys stored securely
- **CORS Configuration**: Proper cross-origin resource sharing setup

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
npm test
```

### API Testing
Use the provided Postman collection or test endpoints directly:
```bash
curl -X GET http://localhost:8000/api/tasks/
curl -X POST http://localhost:8000/api/ai/capabilities/
```

## 📝 Development Notes

### Code Quality
- **Type Safety**: Full TypeScript implementation
- **Error Handling**: Comprehensive error handling and user feedback
- **Code Organization**: Modular architecture with clear separation of concerns
- **Documentation**: Extensive inline documentation and comments

### Performance Optimizations
- **Database Indexing**: Proper indexing on frequently queried fields
- **API Pagination**: Efficient data loading with pagination
- **Caching**: Strategic caching for frequently accessed data
- **Lazy Loading**: Components loaded on demand

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Screenshots

image.png
image.png
image.png
image.png-
## 🔮 Future Enhancements

- **Calendar Integration**: Sync with Google Calendar, Outlook
- **Mobile App**: React Native mobile application
- **Team Collaboration**: Multi-user support with shared tasks
- **Advanced Analytics**: Productivity insights and reporting
- **Voice Input**: Voice-to-text for task creation
- **Notification System**: Smart reminders and alerts
- **Export/Import**: Data backup and migration tools
- **Dark Mode**: Complete dark theme implementation
- **Offline Support**: Progressive Web App capabilities

---

**Thank You**
