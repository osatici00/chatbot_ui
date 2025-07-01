"""
Mock API for ChatGPT-Style UI Demo
Provides realistic data analysis responses with interactive charts
All data is completely generic and suitable for public demonstrations
"""

import os
import json
import asyncio
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
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

# Progress logging system
class ProgressLogger:
    def __init__(self):
        self.logs_dir = "logs"
        self.active_connections: Dict[str, WebSocket] = {}
        self.session_progress: Dict[str, List[Dict]] = {}
        self.session_notifications: Dict[str, Dict] = {}
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def get_log_file_path(self, session_id: str) -> str:
        return os.path.join(self.logs_dir, f"{session_id}_progress.json")
    
    async def log_progress(self, session_id: str, step: str, message: str, step_number: int = None, total_steps: int = None):
        """Log progress step and notify connected clients"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "step": step,
            "message": message,
            "step_number": step_number,
            "total_steps": total_steps,
            "session_id": session_id
        }
        
        # Store in memory for active sessions
        if session_id not in self.session_progress:
            self.session_progress[session_id] = []
        self.session_progress[session_id].append(log_entry)
        
        # Write to file
        log_file = self.get_log_file_path(session_id)
        try:
            # Read existing logs
            existing_logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    existing_logs = json.load(f)
            
            # Append new log
            existing_logs.append(log_entry)
            
            # Write back
            with open(log_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)
        except Exception as e:
            print(f"Error writing log file: {e}")
        
        # Send to connected WebSocket clients
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(log_entry))
            except Exception as e:
                print(f"Error sending WebSocket message: {e}")
                # Remove failed connection
                if session_id in self.active_connections:
                    del self.active_connections[session_id]
    
    def add_notification(self, session_id: str, message: str):
        """Add notification for completed responses in background"""
        self.session_notifications[session_id] = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
    
    def get_notifications(self, session_id: str) -> Dict:
        """Get notifications for a session"""
        return self.session_notifications.get(session_id, {})
    
    def mark_notification_read(self, session_id: str):
        """Mark notification as read"""
        if session_id in self.session_notifications:
            self.session_notifications[session_id]["read"] = True
    
    def get_progress_logs(self, session_id: str) -> List[Dict]:
        """Get all progress logs for a session"""
        # Try memory first
        if session_id in self.session_progress:
            return self.session_progress[session_id]
        
        # Fall back to file
        log_file = self.get_log_file_path(session_id)
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading log file: {e}")
        
        return []

# Global progress logger instance
progress_logger = ProgressLogger()

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
    has_notification: bool = False

# In-memory storage
sessions = {}
uploaded_files = {}

async def simulate_analysis_with_progress(session_id: str, user_query: str, response_type: str):
    """Simulate analysis process with realistic progress steps"""
    
    # Define progress steps based on response type
    if response_type == "chart":
        steps = [
            ("Scanning databases", "Connecting to data sources and scanning available datasets..."),
            ("Analyzing data", "Processing and analyzing data patterns..."),
            ("Fetching relevant data", "Retrieving specific data points for visualization..."),
            ("Generating visualization", "Creating interactive chart based on analysis..."),
            ("Preparing response", "Finalizing response with insights and recommendations...")
        ]
    elif response_type == "file":
        steps = [
            ("Scanning databases", "Accessing database connections..."),
            ("Fetching relevant data", "Querying databases for requested information..."),
            ("Processing data", "Cleaning and formatting data for export..."),
            ("Generating file", "Creating downloadable file with processed data..."),
            ("Preparing download", "Finalizing file and preparing download link...")
        ]
    else:  # text analysis
        steps = [
            ("Scanning databases", "Connecting to data sources..."),
            ("Analyzing patterns", "Identifying trends and patterns in the data..."),
            ("Fetching insights", "Extracting key insights and metrics..."),
            ("Generating analysis", "Compiling comprehensive analysis report..."),
            ("Preparing response", "Formatting final response with recommendations...")
        ]
    
    total_steps = len(steps)
    
    for i, (step_name, step_message) in enumerate(steps, 1):
        await progress_logger.log_progress(
            session_id=session_id,
            step=step_name,
            message=step_message,
            step_number=i,
            total_steps=total_steps
        )
        
        # Simulate processing time (random between 1-3 seconds)
        await asyncio.sleep(random.uniform(1.0, 3.0))
    
    # Final completion log
    await progress_logger.log_progress(
        session_id=session_id,
        step="Completed",
        message="Analysis completed successfully!",
        step_number=total_steps,
        total_steps=total_steps
    )

def generate_chart_data(requested_type: str = None):
    """Generate interactive chart data for different visualization types"""
    chart_types = ["bar", "line", "pie", "scatter"]
    
    # Use requested type if provided, otherwise random
    if requested_type and requested_type in chart_types:
        chart_type = requested_type
    else:
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

def determine_chart_type(user_query: str) -> str:
    """Determine specific chart type from user query"""
    query_lower = user_query.lower()
    
    if any(keyword in query_lower for keyword in ["bar chart", "bar graph", "column chart", "histogram"]):
        return "bar"
    elif any(keyword in query_lower for keyword in ["line chart", "line graph", "trend", "time series"]):
        return "line"
    elif any(keyword in query_lower for keyword in ["pie chart", "pie graph", "donut", "distribution"]):
        return "pie"
    elif any(keyword in query_lower for keyword in ["scatter plot", "scatter chart", "correlation", "scatter"]):
        return "scatter"
    else:
        return None  # No specific type requested

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
async def query_endpoint(request: QueryRequest):
    """Main query endpoint - simulates realistic AI analysis with progress logging"""
    
    # Generate session ID
    session_id = request.session_id or str(uuid.uuid4())
    
    # Create session if new
    if session_id not in sessions:
        sessions[session_id] = {
            "session_id": session_id,
            "title": create_session_title(request.user_query),
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "status": "processing",
            "messages": []
        }
    
    # Update session
    sessions[session_id]["last_activity"] = datetime.now().isoformat()
    sessions[session_id]["status"] = "processing"
    sessions[session_id]["messages"].append({
        "type": "user",
        "content": request.user_query,
        "timestamp": datetime.now().isoformat()
    })
    
    # Determine response type based on query
    response_type = determine_response_type(request.user_query)
    
    # Start background processing with progress logging
    asyncio.create_task(process_query_with_progress(session_id, request.user_query, response_type))
    
    # Return immediate response indicating processing has started
    return QueryResponse(
        session_id=session_id,
        status="processing",
        message="Your request is being processed. Progress updates will be shown in real-time.",
        response_type=response_type
    )

async def process_query_with_progress(session_id: str, user_query: str, response_type: str):
    """Process query in background with progress updates"""
    try:
        # Start progress logging
        await progress_logger.log_progress(
            session_id=session_id,
            step="Starting",
            message="Starting analysis of your request...",
            step_number=0,
            total_steps=5
        )
        
        # Simulate analysis with progress
        await simulate_analysis_with_progress(session_id, user_query, response_type)
        
        # Generate final response based on type
        if response_type == "chart":
            requested_chart_type = determine_chart_type(user_query)
            chart_data = generate_chart_data(requested_chart_type)
            response_content = generate_mock_text_response()
            
            sessions[session_id]["messages"].append({
                "type": "assistant", 
                "content": response_content,
                "chart_data": chart_data,
                "timestamp": datetime.now().isoformat()
            })
            
        elif response_type == "file":
            file_info = generate_mock_file_response()
            response_content = f"Your {file_info['file_type'].upper()} report has been generated and is ready for download."
            
            sessions[session_id]["messages"].append({
                "type": "assistant",
                "content": response_content,
                "file_info": file_info,
                "timestamp": datetime.now().isoformat()
            })
            
        else:  # text response
            response_content = generate_mock_text_response()
            sessions[session_id]["messages"].append({
                "type": "assistant", 
                "content": response_content,
                "timestamp": datetime.now().isoformat()
            })
        
        # Update session status
        sessions[session_id]["status"] = "completed"
        sessions[session_id]["last_activity"] = datetime.now().isoformat()
        
        # Add notification for background completion
        progress_logger.add_notification(
            session_id=session_id,
            message="Analysis completed!"
        )
        
        # Final completion log
        await progress_logger.log_progress(
            session_id=session_id,
            step="Finished",
            message="Response ready! Check your chat for the complete analysis.",
            step_number=6,
            total_steps=6
        )
        
    except Exception as e:
        print(f"Error processing query: {e}")
        sessions[session_id]["status"] = "error"
        await progress_logger.log_progress(
            session_id=session_id,
            step="Error",
            message=f"An error occurred: {str(e)}",
            step_number=0,
            total_steps=0
        )

@app.websocket("/ws/progress/{session_id}")
async def websocket_progress(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time progress updates"""
    await websocket.accept()
    progress_logger.active_connections[session_id] = websocket
    
    try:
        # Send existing progress logs when client connects
        existing_logs = progress_logger.get_progress_logs(session_id)
        for log in existing_logs:
            await websocket.send_text(json.dumps(log))
        
        # Keep connection alive
        while True:
            try:
                await websocket.receive_text()
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"WebSocket error: {e}")
                break
    except WebSocketDisconnect:
        pass
    finally:
        if session_id in progress_logger.active_connections:
            del progress_logger.active_connections[session_id]

@app.get("/api/progress/{session_id}")
async def get_progress(session_id: str):
    """Get progress logs for a session"""
    logs = progress_logger.get_progress_logs(session_id)
    return {"session_id": session_id, "logs": logs}

@app.get("/api/sessions", response_model=List[SessionInfo])
def get_sessions():
    """Get all user sessions with notification status"""
    session_list = []
    for session in sessions.values():
        # Check if session has unread notifications
        notification = progress_logger.get_notifications(session["session_id"])
        has_notification = notification and not notification.get("read", True)
        
        session_list.append(SessionInfo(
            session_id=session["session_id"],
            title=session["title"],
            created_at=session["created_at"],
            last_activity=session["last_activity"],
            status=session["status"],
            has_notification=has_notification
        ))
    
    return session_list

@app.get("/api/sessions/{session_id}")
def get_session(session_id: str):
    """Get specific session details and mark notifications as read"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Mark notifications as read when session is accessed
    progress_logger.mark_notification_read(session_id)
    
    session_data = sessions[session_id].copy()
    session_data["notification"] = progress_logger.get_notifications(session_id)
    return session_data

@app.post("/api/sessions/{session_id}/mark-read")
def mark_notification_read(session_id: str):
    """Mark session notifications as read"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    progress_logger.mark_notification_read(session_id)
    return {"message": "Notification marked as read"}

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