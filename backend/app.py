"""
Mock API for ChatGPT-Style UI Demo
Provides realistic data analysis responses with interactive charts
All data is completely generic and suitable for public demonstrations
"""

import os
import uuid
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import random
from faker import Faker

# Initialize
app = FastAPI(title="ChatGPT UI Demo API", version="1.0.0")
fake = Faker()

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    user_query: str
    user_email: str
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    session_id: str
    status: str
    message: str
    response_content: Optional[str] = None
    response_type: str = "text"
    file_info: Optional[Dict[str, Any]] = None
    progress: Optional[Dict[str, Any]] = None
    chart_data: Optional[Dict[str, Any]] = None

class SessionInfo(BaseModel):
    session_id: str
    title: str
    created_at: str
    last_activity: str
    status: str

# In-memory storage
sessions = {}
uploaded_files = {}

def generate_chart_data():
    """Generate interactive chart data for different visualization types"""
    chart_types = ["bar", "line", "pie", "scatter"]
    chart_type = random.choice(chart_types)
    
    if chart_type == "bar":
        return {
            "type": "bar",
            "title": "Revenue by Region - Q1 2024",
            "data": {
                "labels": ["North America", "Europe", "Asia Pacific", "Latin America", "Africa"],
                "datasets": [{
                    "label": "Revenue (Millions $)",
                    "data": [2.4, 1.8, 1.6, 0.9, 0.7],
                    "backgroundColor": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {"position": "top"},
                    "title": {"display": True, "text": "Revenue by Region - Q1 2024"}
                }
            }
        }
    
    elif chart_type == "line":
        # Generate trend data for the last 12 months
        months = []
        satisfaction_scores = []
        current_date = datetime.now()
        
        for i in range(12):
            month_date = current_date - timedelta(days=30*i)
            months.append(month_date.strftime("%b %Y"))
            satisfaction_scores.append(round(random.uniform(3.8, 4.8), 1))
        
        months.reverse()
        satisfaction_scores.reverse()
        
        return {
            "type": "line",
            "title": "Customer Satisfaction Trend - 12 Months",
            "data": {
                "labels": months,
                "datasets": [{
                    "label": "Satisfaction Score",
                    "data": satisfaction_scores,
                    "borderColor": "#3B82F6",
                    "backgroundColor": "rgba(59, 130, 246, 0.1)",
                    "fill": True,
                    "tension": 0.4
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {"position": "top"},
                    "title": {"display": True, "text": "Customer Satisfaction Trend"}
                },
                "scales": {
                    "y": {"min": 3.0, "max": 5.0}
                }
            }
        }
    
    elif chart_type == "pie":
        return {
            "type": "pie",
            "title": "Support Ticket Distribution - Q1 2024",
            "data": {
                "labels": ["Technical Issues", "Account Questions", "Product Inquiries", "Feature Requests", "Bug Reports"],
                "datasets": [{
                    "data": [31, 23, 18, 16, 12],
                    "backgroundColor": ["#EF4444", "#F59E0B", "#10B981", "#3B82F6", "#8B5CF6"]
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {"position": "right"},
                    "title": {"display": True, "text": "Support Ticket Distribution"}
                }
            }
        }
    
    else:  # scatter
        # Generate correlation data
        data_points = []
        for _ in range(50):
            x = random.uniform(1000, 10000)  # Order value
            y = x * random.uniform(0.3, 0.7) + random.uniform(-500, 500)  # Customer satisfaction correlation
            data_points.append({"x": round(x, 2), "y": round(y, 2)})
        
        return {
            "type": "scatter",
            "title": "Order Value vs Customer Satisfaction",
            "data": {
                "datasets": [{
                    "label": "Customer Data Points",
                    "data": data_points,
                    "backgroundColor": "#3B82F6",
                    "borderColor": "#1D4ED8"
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {"position": "top"},
                    "title": {"display": True, "text": "Order Value vs Customer Satisfaction"}
                },
                "scales": {
                    "x": {"title": {"display": True, "text": "Order Value ($)"}},
                    "y": {"title": {"display": True, "text": "Satisfaction Score"}}
                }
            }
        }

def generate_mock_text_response():
    """Generate realistic analysis response text with completely generic data"""
    responses = [
        """## Customer Satisfaction Analysis - Q1 2024

**Key Findings:**
- Overall satisfaction score: 4.2/5.0 (up 8% from Q4 2023)
- Top performing agents: Agent A (4.8), Agent B (4.6)
- Response time improved by 15% this quarter
- Main issues: Technical support (23%), Account questions (31%)

**Recommendations:**
1. Expand technical support team
2. Improve help documentation
3. Continue current training programs

**Data Sources:** 1,247 customer surveys, 892 support tickets

*Interactive chart showing trend analysis is displayed above.*""",
        
        """## Sales Performance Dashboard - Q1 2024

**Revenue Metrics:**
- Total Revenue: $2.4M (target: $2.1M) ✅
- New Customers: 156 (up 23% YoY)
- Customer Retention: 94.2%
- Average Deal Size: $15,400

**Regional Performance:**
1. **North America**: $2.4M (35% of total) - Exceeded targets
2. **Europe**: $1.8M (26% of total) - On track
3. **Asia Pacific**: $1.6M (23% of total) - Strong growth
4. **Latin America**: $0.9M (13% of total) - Improving
5. **Africa**: $0.7M (10% of total) - New market

**Growth Areas:**
- Enterprise segment showing 45% growth
- Small business segment down 12%
- Mobile engagement up 67%

*Revenue breakdown by region shown in the interactive chart above.*""",
        
        """## Data Quality Report - Comprehensive Analysis

**Analysis Complete:** ✅

**Data Sources Analyzed:**
- ABC Database: 12,447 records
- XYZ Database: 8,932 records  
- Survey Database: 1,247 responses

**Quality Metrics:**
- **Completeness**: 96.8% (Target: >95%) ✅
- **Accuracy**: 94.2% (Target: >90%) ✅
- **Consistency**: 98.1% (Target: >95%) ✅

**Issues Identified & Resolved:**
- 47 duplicate records (cleaned automatically)
- 12 missing email addresses (flagged for manual review)
- 3 data format inconsistencies (standardized)

**Recommendations:**
1. Implement real-time validation for email fields
2. Add duplicate detection rules
3. Schedule weekly quality checks

All data quality checks passed. Dataset ready for production analysis.

*Data quality distribution shown in the interactive chart above.*"""
    ]
    return random.choice(responses)

def generate_mock_file_response():
    """Generate mock file download info"""
    file_types = ["excel", "pdf", "csv"]
    file_type = random.choice(file_types)
    
    return {
        "filename": f"analysis_report_{fake.date()}.{file_type}",
        "download_url": f"/api/download/{uuid.uuid4()}",
        "file_type": file_type,
        "file_size": f"{random.randint(100, 5000)} KB"
    }

def create_session_title(user_query: str) -> str:
    """Create a meaningful session title from user query"""
    if len(user_query) <= 50:
        return user_query
    return user_query[:47] + "..."

def determine_response_type(user_query: str) -> str:
    """Determine response type based on query content"""
    query_lower = user_query.lower()
    
    # File/Excel download keywords
    file_keywords = ["excel", "download", "export", "spreadsheet", "csv file", "generate report"]
    
    # Progress/status keywords
    progress_keywords = ["status", "progress", "processing", "loading"]
    
    # Chart-specific keywords
    chart_keywords = ["chart", "graph", "plot", "visualize", "bar chart", "line chart", "pie chart", "scatter plot"]
    
    # Text analysis keywords
    text_keywords = ["analyze", "summary", "insights", "findings", "report", "analysis"]
    
    # Check for specific response types
    if any(keyword in query_lower for keyword in file_keywords):
        print(f"DEBUG: File request detected in '{user_query}' - returning file")
        return "file"
    elif any(keyword in query_lower for keyword in progress_keywords):
        print(f"DEBUG: Progress request detected in '{user_query}' - returning progress")
        return "progress"
    elif any(keyword in query_lower for keyword in chart_keywords):
        print(f"DEBUG: Chart request detected in '{user_query}' - returning chart")
        return "chart"
    elif any(keyword in query_lower for keyword in text_keywords):
        print(f"DEBUG: Text analysis request detected in '{user_query}' - returning text")
        return "text"
    else:
        # Default to chart for demo purposes
        print(f"DEBUG: Defaulting to chart for '{user_query}'")
        return "chart"

@app.get("/")
def root():
    """Health check"""
    return {"message": "ChatGPT UI Demo API is running", "timestamp": datetime.now().isoformat()}

@app.post("/api/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    """Main query endpoint - simulates realistic AI analysis"""
    
    # Generate session ID
    session_id = request.session_id or str(uuid.uuid4())
    
    # Create session if new
    if session_id not in sessions:
        sessions[session_id] = {
            "session_id": session_id,
            "title": create_session_title(request.user_query),
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "status": "active",
            "messages": []
        }
    
    # Update session
    sessions[session_id]["last_activity"] = datetime.now().isoformat()
    sessions[session_id]["messages"].append({
        "type": "user",
        "content": request.user_query,
        "timestamp": datetime.now().isoformat()
    })
    
    # Determine response type based on query
    response_type = determine_response_type(request.user_query)
    
    if response_type == "chart":
        chart_data = generate_chart_data()
        response_content = generate_mock_text_response()
        
        sessions[session_id]["messages"].append({
            "type": "assistant", 
            "content": response_content,
            "chart_data": chart_data,
            "timestamp": datetime.now().isoformat()
        })
        
        return QueryResponse(
            session_id=session_id,
            status="completed",
            message="Analysis with interactive chart generated successfully",
            response_content=response_content,
            response_type="chart",
            chart_data=chart_data
        )
    
    elif response_type == "file":
        file_info = generate_mock_file_response()
        response_content = f"Your {file_info['file_type'].upper()} report has been generated and is ready for download."
        
        sessions[session_id]["messages"].append({
            "type": "assistant",
            "content": response_content,
            "file_info": file_info,
            "timestamp": datetime.now().isoformat()
        })
        
        return QueryResponse(
            session_id=session_id,
            status="completed", 
            message="File generated successfully",
            response_content=response_content,
            response_type="file",
            file_info=file_info
        )
    
    elif response_type == "progress":
        return QueryResponse(
            session_id=session_id,
            status="processing",
            message="Analyzing data from multiple sources...",
            response_type="progress",
            progress={
                "current_step": "Data fetching",
                "total_steps": 5,
                "percentage": random.randint(10, 90)
            }
        )
    
    else:  # text response
        response_content = generate_mock_text_response()
        sessions[session_id]["messages"].append({
            "type": "assistant", 
            "content": response_content,
            "timestamp": datetime.now().isoformat()
        })
        
        return QueryResponse(
            session_id=session_id,
            status="completed",
            message="Analysis completed successfully",
            response_content=response_content,
            response_type="text"
        )

@app.get("/api/sessions", response_model=List[SessionInfo])
def get_sessions():
    """Get all user sessions"""
    return [
        SessionInfo(
            session_id=session["session_id"],
            title=session["title"],
            created_at=session["created_at"],
            last_activity=session["last_activity"],
            status=session["status"]
        )
        for session in sessions.values()
    ]

@app.get("/api/sessions/{session_id}")
def get_session(session_id: str):
    """Get specific session details"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    """Delete a session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    del sessions[session_id]
    return {"message": "Session deleted successfully"}

@app.post("/api/upload")
def upload_file(file: UploadFile = File(...)):
    """Handle file uploads"""
    file_id = str(uuid.uuid4())
    uploaded_files[file_id] = {
        "filename": file.filename,
        "content_type": file.content_type,
        "upload_time": datetime.now().isoformat()
    }
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "message": f"File '{file.filename}' uploaded successfully",
        "status": "uploaded"
    }

@app.get("/api/download/{file_id}")
def download_file(file_id: str):
    """Mock file download"""
    return {"message": f"Download link for file {file_id}", "url": f"/files/{file_id}"}

@app.get("/api/status/{session_id}")
def get_status(session_id: str):
    """Get session status"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    return {
        "session_id": session_id,
        "status": session["status"],
        "message": "Session is active",
        "last_activity": session["last_activity"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 