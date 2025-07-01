# ChatGPT-Style UI Demo with Interactive Charts

A modern **ChatGPT-like interface** with **interactive data visualizations** for showcasing AI-powered data analysis capabilities.

## 🎯 Overview

This is a **standalone demo project** featuring:
- **React Frontend**: Modern ChatGPT-style chat interface
- **Mock Backend**: FastAPI server with realistic data analysis responses
- **Interactive Charts**: Chart.js visualizations (bar, line, pie, scatter)
- **Complete UI/UX**: Session management, file uploads, responsive design

Perfect for **demonstrating data analysis AI capabilities** without requiring actual database connections or AI models.

## ✨ Features

### 💬 Chat Interface
- **ChatGPT-style UI** with message bubbles and auto-scroll
- **Session Management** with search and conversation history
- **File Upload** support (CSV, PDF, Excel)
- **Real-time messaging** with loading states and animations
- **Mobile responsive** design

### 📊 Interactive Visualizations
- **4 Chart Types**: Bar charts, line graphs, pie charts, scatter plots
- **Smart Detection**: Automatically generates charts based on query keywords
- **Interactive Features**: Hover tooltips, legend toggles, zoom/pan
- **Professional Styling**: Business-ready color scheme and animations
- **Responsive Charts**: Optimized for all screen sizes

### 🎭 Mock Data & Responses
- **Realistic Business Scenarios**: Customer analytics, sales performance, data quality
- **Mixed Content Types**: Charts + analysis text, file downloads, progress indicators
- **Generic Data**: No company-specific information, suitable for public demos
- **Variety**: Multiple response types for comprehensive testing

## 🚀 Quick Start

### Prerequisites
- **Node.js 16+** for React frontend
- **Python 3.8+** for Mock API
- **npm or yarn** package manager

### Installation

```bash
# Clone and navigate to project
cd chatgpt-ui-demo

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies  
cd ../backend
pip install -r requirements.txt
```

### Running the Demo

**Option 1: Use Start Scripts**
```bash
# Windows
.\start.bat

# Mac/Linux
chmod +x start.sh && ./start.sh
```

**Option 2: Manual Start**
```bash
# Terminal 1: Start Backend
cd backend
python app.py
# → Backend running on http://localhost:8001

# Terminal 2: Start Frontend
cd frontend  
npm run dev
# → Frontend running on http://localhost:3000
```

### Access the Demo
1. **Open Browser**: http://localhost:3000
2. **Try Chart Queries**: Use the examples below
3. **Explore Features**: Upload files, manage sessions, test responsiveness

## 💡 Demo Queries

### Chart Generation Examples
```bash
📊 "Show me a revenue chart by region"
📈 "Customer satisfaction trend over 12 months"  
🥧 "Support ticket distribution pie chart"
⚫ "Revenue vs customer satisfaction scatter plot"
📊 "Create a bar chart of quarterly performance"
📈 "Visualize sales trends"
```

### Other Response Types
```bash
📄 "Generate a quarterly report"
📥 "Download performance data"
⏳ "Check processing status"
📊 "Analyze uploaded data" (after file upload)
```

## 🎨 Technology Stack

### Frontend
- **React 18** with hooks and modern patterns
- **Vite** for fast development and building
- **Tailwind CSS** for styling and responsive design
- **Chart.js + react-chartjs-2** for interactive visualizations
- **Axios** for API communication
- **React Markdown** for rich text rendering

### Backend
- **FastAPI** for high-performance async API
- **Chart.js Data Format** for visualization responses
- **Realistic Mock Data** generation
- **CORS** enabled for frontend development

## 📊 Chart Types & Data

### Bar Charts
- **Use Case**: Category comparisons, regional performance
- **Sample Data**: Revenue by region, performance by department
- **Features**: Colorful bars, hover tooltips, responsive scaling

### Line Charts  
- **Use Case**: Time series analysis, trend identification
- **Sample Data**: 12-month satisfaction trends, sales growth
- **Features**: Smooth curves, filled areas, zoom capabilities

### Pie Charts
- **Use Case**: Distribution analysis, percentage breakdowns  
- **Sample Data**: Support ticket categories, market share
- **Features**: Interactive legend, hover percentages

### Scatter Plots
- **Use Case**: Correlation analysis, relationship studies
- **Sample Data**: Revenue vs satisfaction, engagement vs retention
- **Features**: 50+ data points, correlation patterns

## 🔧 Project Structure

```
chatgpt-ui-demo/
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ChatArea.jsx          # Main chat interface
│   │   │   ├── Sidebar.jsx           # Session management
│   │   │   ├── MessageList.jsx       # Message display
│   │   │   ├── AssistantMessage.jsx  # AI response component
│   │   │   ├── UserMessage.jsx       # User message component
│   │   │   ├── ChartDisplay.jsx      # Interactive chart rendering
│   │   │   ├── FileUpload.jsx        # File upload interface
│   │   │   └── LoadingMessage.jsx    # Loading states
│   │   ├── services/          # API communication
│   │   ├── styles/            # CSS and styling
│   │   └── App.jsx            # Main application
│   ├── package.json           # Dependencies
│   ├── vite.config.js         # Build configuration
│   └── tailwind.config.js     # Styling configuration
│
├── backend/                    # Mock API server
│   ├── app.py                 # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── uploads/               # File upload directory
│
├── docs/                       # Documentation
├── start.bat                   # Windows start script
├── start.sh                    # Unix start script
└── README.md                   # This file
```

## 🎯 Use Cases

### Demo & Presentation
- **Product Demos**: Showcase AI data analysis capabilities
- **Client Presentations**: Interactive demonstration of features
- **Prototype Testing**: UI/UX validation before backend integration
- **Training**: Familiarize teams with the interface design

### Development
- **Frontend Development**: Build and test UI components independently  
- **API Design**: Validate request/response formats
- **Performance Testing**: Stress test the frontend with various data
- **Integration Planning**: Plan real backend integration

### Marketing & Sales
- **Website Integration**: Embed interactive demo
- **Trade Shows**: Live demonstration tool
- **Case Studies**: Generate realistic screenshots and videos
- **User Testing**: Gather feedback on interface design

## 🛠️ Customization

### Branding & Styling
```javascript
// frontend/tailwind.config.js - Update colors
theme: {
  extend: {
    colors: {
      primary: '#your-brand-color',
      secondary: '#your-secondary-color'
    }
  }
}
```

### Mock Data
```python
# backend/app.py - Add your data scenarios
def generate_custom_data():
    return {
        "type": "bar",
        "title": "Your Custom Analysis",
        "data": { /* your data */ }
    }
```

### API Endpoints
```javascript
// frontend/src/services/api.js - Update for production
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api.com/api'
  : '/api'
```

## 🔒 Generic Data Notice

All mock data in this demo is **completely generic**:
- No real company names, databases, or proprietary information
- Sample data uses placeholder names and fictional scenarios
- Safe for public repositories and demonstrations
- Realistic but not based on actual business data

## 📱 Responsive Design

- **Desktop**: Full-featured interface with charts and sidebar
- **Tablet**: Optimized layout with collapsible sidebar
- **Mobile**: Touch-friendly interface with responsive charts
- **Cross-browser**: Tested on Chrome, Firefox, Safari, Edge

## 🔄 Development Workflow

1. **Frontend Development**: Use mock API for rapid UI iteration
2. **API Testing**: Validate response formats and error handling
3. **Integration**: Replace mock endpoints with real backend
4. **Deployment**: Build production-ready application

## 🐛 Troubleshooting

### Common Issues
- **Port Conflicts**: Change ports in configuration files
- **Chart Rendering**: Check browser console for Chart.js errors  
- **CORS Issues**: Verify backend CORS configuration
- **File Uploads**: Check file size limits and supported types

### Debug Mode
Backend includes debug logging:
```
DEBUG: Chart keyword detected in 'show revenue chart' - returning chart
```

## 📄 License

This demo project is provided as-is for demonstration and development purposes.

---

**🎉 Ready to showcase your AI-powered data analysis capabilities!**

*A complete, interactive demonstration platform for modern data analysis interfaces.* 