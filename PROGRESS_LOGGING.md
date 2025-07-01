# Progress Logging System

This document describes the real-time progress logging system implemented in the ChatGPT UI Demo. The system provides live updates to users while their requests are being processed in the background, similar to how ChatGPT shows its thinking process.

## Features

### 🔄 Real-time Progress Updates
- **Live Progress Logs**: Shows step-by-step progress while the API processes requests
- **WebSocket Connection**: Real-time updates without polling
- **Animated UI**: Smooth animations and progress bars for each step
- **Connection Status**: Visual indicator of WebSocket connection status

### 📋 Progress Steps
Different request types show different progress steps:

**Chart Generation:**
1. Scanning databases
2. Analyzing data
3. Fetching relevant data
4. Generating visualization
5. Preparing response

**File Generation:**
1. Scanning databases
2. Fetching relevant data
3. Processing data
4. Generating file
5. Preparing download

**Text Analysis:**
1. Scanning databases
2. Analyzing patterns
3. Fetching insights
4. Generating analysis
5. Preparing response

### 🔔 Background Notifications
- **Notification Dots**: Shows blue dots on completed background sessions
- **Auto-refresh**: Sessions list updates every 5 seconds
- **Read Status**: Notifications are marked as read when session is accessed
- **Persistent Storage**: Notifications survive server restarts

## Architecture

### Backend Components

#### ProgressLogger Class
```python
class ProgressLogger:
    def __init__(self):
        self.logs_dir = "logs"
        self.active_connections: Dict[str, WebSocket] = {}
        self.session_progress: Dict[str, List[Dict]] = {}
        self.session_notifications: Dict[str, Dict] = {}
```

**Key Methods:**
- `log_progress()`: Logs progress steps and notifies WebSocket clients
- `add_notification()`: Creates notifications for completed responses
- `get_progress_logs()`: Retrieves all logs for a session
- `mark_notification_read()`: Marks notifications as read

#### WebSocket Endpoint
```
/ws/progress/{session_id}
```
- Accepts WebSocket connections for real-time progress updates
- Sends existing logs when client connects
- Maintains active connections for live updates

#### API Endpoints
```
GET /api/progress/{session_id}        # Get progress logs
GET /api/sessions                     # Get sessions with notification status
POST /api/sessions/{session_id}/mark-read  # Mark notification as read
```

### Frontend Components

#### ProgressLogger Component
Location: `frontend/src/components/ProgressLogger.jsx`

**Features:**
- WebSocket connection management
- Real-time log display with animations
- Progress bars for each step
- Connection status indicator
- Auto-scroll to latest logs

**Props:**
- `sessionId`: Session to monitor
- `isVisible`: Whether to show the component
- `onComplete`: Callback when processing completes

#### Updated Components
- **ChatArea**: Integrates ProgressLogger for real-time updates
- **Sidebar**: Shows notification dots for completed responses
- **App**: Handles session refresh and notification management

## File Storage

### Log Files
- **Location**: `backend/logs/`
- **Format**: `{session_id}_progress.json`
- **Content**: Array of log entries with timestamps, steps, and messages

### Log Entry Structure
```json
{
  "timestamp": "2024-07-01T17:30:45.123456",
  "step": "Analyzing data",
  "message": "Processing and analyzing data patterns...",
  "step_number": 2,
  "total_steps": 5,
  "session_id": "uuid-here"
}
```

## Usage

### For Users
1. **Submit a Request**: Type any query and press Send
2. **Watch Progress**: Real-time progress logs appear below the chat
3. **Background Processing**: Switch to other chats while processing continues
4. **Notifications**: Blue dots appear on sessions with completed responses
5. **View Results**: Click on sessions with dots to see completed responses

### For Developers

#### Adding New Progress Steps
```python
await progress_logger.log_progress(
    session_id=session_id,
    step="Custom Step",
    message="Detailed description of what's happening",
    step_number=1,
    total_steps=5
)
```

#### Creating Notifications
```python
progress_logger.add_notification(
    session_id=session_id,
    message="Custom notification message"
)
```

#### Checking Connection Status
```javascript
// In React component
const [isConnected, setIsConnected] = useState(false)

wsRef.current.onopen = () => {
  setIsConnected(true)
}
```

## Configuration

### WebSocket Settings
- **URL**: `ws://localhost:8001/ws/progress/{session_id}`
- **Reconnection**: Automatic on connection loss
- **Timeout**: 30 seconds for initial connection

### Refresh Intervals
- **Session List**: Every 5 seconds
- **Progress Updates**: Real-time via WebSocket
- **Notification Check**: On session access

### Storage Settings
- **Log Directory**: `backend/logs/` (auto-created)
- **File Format**: JSON with UTF-8 encoding
- **Retention**: Logs persist until manually deleted

## Performance Considerations

### Memory Management
- Active connections cleaned up on disconnect
- Progress logs cached in memory for active sessions
- File-based storage for persistence

### Scalability
- WebSocket connections per session
- Asynchronous processing with asyncio
- Efficient JSON serialization

### Error Handling
- Connection failures gracefully handled
- Automatic reconnection attempts
- Fallback to HTTP polling if WebSocket fails

## Testing

### Test Script
Run the comprehensive test suite:
```bash
cd backend
python test_progress_logging.py
```

**Test Coverage:**
- Basic progress logging
- Full analysis simulation
- File creation and retrieval
- Memory vs file storage
- Notification system
- Different response types

### Manual Testing
1. Start the backend server
2. Submit a request in the UI
3. Verify real-time progress appears
4. Switch to another chat
5. Confirm notification dot appears when complete
6. Check log files in `backend/logs/`

## Browser Compatibility

### WebSocket Support
- **Chrome**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support

### Fallback Strategy
If WebSocket fails:
1. Component shows connection error
2. Falls back to periodic HTTP requests
3. User can refresh to see final results

## Security Considerations

### WebSocket Security
- Connection limited to localhost in development
- Session ID validation required
- No sensitive data in progress messages

### File Storage Security
- Logs stored locally only
- Generic progress messages (no sensitive data)
- Files can be safely deleted

## Future Enhancements

### Planned Features
- [ ] Database integration for persistent storage
- [ ] Progress estimation with time remaining
- [ ] Custom progress step definitions
- [ ] Progress sharing between sessions
- [ ] Real-time collaboration features

### Performance Improvements
- [ ] Redis for session state management
- [ ] WebSocket clustering for multiple servers
- [ ] Progress log compression
- [ ] Batch WebSocket updates

## Troubleshooting

### Common Issues

**WebSocket Connection Failed**
- Check if backend server is running
- Verify port 8001 is accessible
- Check browser console for errors

**Progress Not Updating**
- Verify WebSocket connection status
- Check network connectivity
- Refresh the page to reconnect

**Notifications Not Appearing**
- Check session refresh interval
- Verify backend is marking notifications correctly
- Clear browser cache if needed

**Log Files Not Created**
- Check write permissions in `backend/logs/`
- Verify backend has disk space
- Check server console for errors

### Debug Commands
```bash
# Check WebSocket connections
netstat -an | findstr "8001"

# View log files
ls backend/logs/
cat backend/logs/{session_id}_progress.json

# Test progress system
python backend/test_progress_logging.py
```

## API Reference

### WebSocket Messages

**Incoming (from server):**
```json
{
  "timestamp": "ISO-8601-timestamp",
  "step": "step-name",
  "message": "human-readable-message",
  "step_number": 1,
  "total_steps": 5,
  "session_id": "session-uuid"
}
```

**Outgoing (to server):**
- Keep-alive pings (handled automatically)
- Connection close notifications

### REST API

**GET /api/progress/{session_id}**
```json
{
  "session_id": "uuid",
  "logs": [
    {
      "timestamp": "...",
      "step": "...",
      "message": "...",
      "step_number": 1,
      "total_steps": 5
    }
  ]
}
```

**GET /api/sessions**
```json
[
  {
    "session_id": "uuid",
    "title": "Session Title",
    "created_at": "timestamp",
    "last_activity": "timestamp",
    "status": "processing|completed|error",
    "has_notification": true
  }
]
```

This progress logging system provides a comprehensive solution for real-time user feedback during API processing, enhancing the user experience with live updates and background notifications. 