# ChatGPT-Style UI Demo

A complete ChatGPT-style user interface with React frontend and FastAPI backend, featuring interactive charts, file uploads, and session management.

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- Git

### Option 1: One-Click Start (Windows)
1. Clone the repository
2. Double-click `start_backend.bat` (installs dependencies & starts backend)
3. Double-click `start_frontend.bat` (starts React frontend)
4. Open http://localhost:5173

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs on: http://localhost:8001

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: http://localhost:5173

## 📋 Features

- **ChatGPT-style Interface**: Clean, modern chat UI
- **Interactive Charts**: Bar, line, pie, and scatter plots using Chart.js
- **File Upload/Download**: Support for CSV, Excel, PDF files
- **Session Management**: Persistent chat sessions with history
- **Real-time Responses**: Multiple response types (text, charts, files, progress)
- **Search**: Search through conversation history
- **Responsive Design**: Works on desktop and mobile

## 🛠 Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Chart.js + react-chartjs-2** - Data visualization
- **Lucide React** - Icons
- **Axios** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Faker** - Mock data generation

## 📡 API Documentation

### Base URL
```
http://localhost:8001
```

### Endpoints

#### 1. Health Check
```http
GET /
```
**Response:**
```json
{
  "message": "ChatGPT UI Demo API is running",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. Send Query
```http
POST /api/query
```
**Request Body:**
```json
{
  "user_query": "Show me a revenue chart by region",
  "user_email": "user@example.com",
  "session_id": "optional-session-id"
}
```
**Response:**
```json
{
  "session_id": "uuid-string",
  "status": "completed",
  "message": "Analysis completed successfully",
  "response_content": "## Analysis Results...",
  "response_type": "chart|text|file|progress",
  "chart_data": {
    "type": "bar",
    "title": "Revenue by Region",
    "data": { "labels": [], "datasets": [] },
    "options": {}
  },
  "file_info": {
    "filename": "report.xlsx",
    "download_url": "/api/download/file-id",
    "file_type": "excel",
    "file_size": "2.5 MB"
  },
  "progress": {
    "current_step": "Processing data",
    "total_steps": 5,
    "percentage": 60
  }
}
```

#### 3. Get All Sessions
```http
GET /api/sessions
```
**Response:**
```json
[
  {
    "session_id": "uuid",
    "title": "Customer analysis discussion",
    "created_at": "2024-01-01T10:00:00",
    "last_activity": "2024-01-01T11:30:00",
    "status": "active"
  }
]
```

#### 4. Get Session Details
```http
GET /api/sessions/{session_id}
```
**Response:**
```json
{
  "session_id": "uuid",
  "title": "Session title",
  "created_at": "2024-01-01T10:00:00",
  "last_activity": "2024-01-01T11:30:00",
  "status": "active",
  "messages": [
    {
      "type": "user|assistant",
      "content": "Message content",
      "timestamp": "2024-01-01T10:05:00",
      "chart_data": {},
      "file_info": {}
    }
  ]
}
```

#### 5. Delete Session
```http
DELETE /api/sessions/{session_id}
```
**Response:**
```json
{
  "message": "Session deleted successfully"
}
```

#### 6. Upload File
```http
POST /api/upload
```
**Request:** Multipart form data with file
**Response:**
```json
{
  "file_id": "uuid",
  "filename": "data.csv",
  "message": "File uploaded successfully",
  "status": "uploaded"
}
```

#### 7. Download File
```http
GET /api/download/{file_id}
```
**Response:**
```json
{
  "message": "Download link for file",
  "url": "/files/file-id"
}
```

## 🎯 Response Types

The API automatically detects query intent and returns appropriate response types:

### Chart Responses
**Triggers:** "chart", "graph", "plot", "visualize", "bar chart", "line chart", "pie chart", "scatter plot"
**Returns:** Interactive Chart.js configuration with data

### File Responses  
**Triggers:** "excel", "download", "export", "spreadsheet", "csv", "generate report"
**Returns:** Download link and file information

### Progress Responses
**Triggers:** "status", "progress", "processing", "loading"
**Returns:** Progress indicator with current step

### Text Responses
**Triggers:** "analyze", "summary", "insights", "findings", "analysis"
**Returns:** Formatted markdown text response

## 🔧 Customization

### Adding New Chart Types
1. Edit `backend/app.py` → `generate_chart_data()` function
2. Add new chart type to `chart_types` array
3. Add corresponding Chart.js configuration

### Modifying Response Logic
1. Edit `backend/app.py` → `determine_response_type()` function
2. Add new keywords to trigger specific response types
3. Update frontend components to handle new response types

### Styling Changes
1. Edit `frontend/src/styles/index.css` for global styles
2. Modify Tailwind classes in React components
3. Update `tailwind.config.js` for theme customization

## 📁 Project Structure

```
chatgpt-ui-demo/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── tests/             # Backend tests
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   └── styles/        # CSS files
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration
├── docs/                  # Documentation
├── start_backend.bat      # Windows backend starter
├── start_frontend.bat     # Windows frontend starter
└── README.md             # This file
```

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check port 8001 is available: `netstat -an | find "8001"`

### Frontend won't start
- Ensure Node.js is installed: `node --version`
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### API connection issues
- Verify backend is running on http://localhost:8001
- Check browser console for CORS errors
- Ensure firewall allows local connections

### Charts not displaying
- Check browser console for Chart.js errors
- Verify chart data format matches Chart.js expectations
- Clear browser cache and reload

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review browser console for errors
3. Verify all dependencies are installed correctly
4. Create an issue in the repository with detailed error information 