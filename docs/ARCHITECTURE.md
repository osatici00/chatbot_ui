# Architecture Overview

## System Components

### Frontend (React)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS for modern design
- **Charts**: Chart.js + react-chartjs-2 for interactive visualizations
- **State Management**: React hooks (useState, useEffect)
- **API Communication**: Axios with interceptors

### Backend (FastAPI)
- **Framework**: FastAPI for high-performance API
- **Mock Data**: Faker library for realistic data generation
- **Response Types**: Text, Charts, Files, Progress indicators
- **Session Management**: In-memory storage for demo purposes

## Component Architecture

```
frontend/src/
├── components/
│   ├── App.jsx                 # Main application component
│   ├── Sidebar.jsx             # Session management & navigation
│   ├── ChatArea.jsx            # Main chat interface
│   ├── MessageList.jsx         # Message display container
│   ├── UserMessage.jsx         # User message bubble
│   ├── AssistantMessage.jsx    # AI response with charts
│   ├── ChartDisplay.jsx        # Interactive chart rendering
│   ├── FileUpload.jsx          # File upload interface
│   └── LoadingMessage.jsx      # Loading state component
├── services/
│   └── api.js                  # API communication layer
└── styles/
    └── index.css               # Global styles & animations
```

## Data Flow

1. **User Input** → ChatArea → API Service
2. **API Processing** → Mock Data Generation → Response
3. **Response Parsing** → Component Rendering → Chart Display
4. **State Updates** → Session Storage → UI Updates

## Chart System

### Chart Types Supported
- **Bar Charts**: Category comparisons, regional data
- **Line Charts**: Time series analysis, trends
- **Pie Charts**: Distribution analysis, percentages
- **Scatter Plots**: Correlation analysis, relationships

### Chart Detection Logic
```python
# Keywords trigger chart responses
chart_keywords = ["chart", "graph", "plot", "visualize", "show", "trend"]
```

### Chart Data Format
```javascript
{
  "type": "bar|line|pie|scatter",
  "title": "Chart Title",
  "data": { /* Chart.js data format */ },
  "options": { /* Chart.js options */ }
}
```

## API Endpoints

### Core Endpoints
- `POST /api/query` - Main chat query processing
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{id}` - Get specific session
- `DELETE /api/sessions/{id}` - Delete session
- `POST /api/upload` - File upload handling

### Response Types
- **text**: Markdown formatted analysis
- **chart**: Interactive visualization + text
- **file**: Downloadable report generation
- **progress**: Processing status updates

## Security Considerations

### Current Implementation (Demo)
- In-memory storage only
- No authentication required
- CORS enabled for development

### Production Recommendations
- Add user authentication (JWT tokens)
- Implement proper session persistence
- Add input validation & sanitization
- Enable HTTPS and secure headers
- Implement rate limiting

## Scalability Notes

### Current Limitations
- In-memory storage (resets on restart)
- Single-threaded processing
- No database persistence

### Production Enhancements
- Database integration (PostgreSQL/MongoDB)
- Redis for session caching
- Background task processing
- Horizontal scaling with load balancer
- CDN for static assets

## Development Workflow

1. **Frontend Development**: Use mock API for rapid iteration
2. **API Testing**: Validate response formats
3. **Chart Integration**: Test interactive features
4. **UI/UX Refinement**: Polish user experience
5. **Production Integration**: Replace mock with real backend 