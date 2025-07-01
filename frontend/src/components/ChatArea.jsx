import React, { useState, useEffect } from 'react'
import MessageList from './MessageList'
import FileUpload from './FileUpload'
import ProgressLogger from './ProgressLogger'
import { Send, Paperclip } from 'lucide-react'
import { sendQuery, getSession } from '../services/api'

function ChatArea({ sessionId, onSessionCreated }) {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showFileUpload, setShowFileUpload] = useState(false)
  const [showProgressLogger, setShowProgressLogger] = useState(false)
  const [currentSessionId, setCurrentSessionId] = useState(sessionId)

  useEffect(() => {
    if (sessionId) {
      loadSession()
      setCurrentSessionId(sessionId)
    } else {
      setMessages([])
      setCurrentSessionId(null)
    }
    setShowProgressLogger(false) // Reset progress logger when switching sessions
  }, [sessionId])

  const loadSession = async () => {
    try {
      const sessionData = await getSession(sessionId)
      setMessages(sessionData.messages || [])
    } catch (error) {
      console.error('Failed to load session:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!inputValue.trim() || isLoading) return

    const userMessage = {
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const response = await sendQuery(
        userMessage.content,
        'demo@example.com',
        sessionId
      )

      // Update current session ID for new sessions
      const responseSessionId = response.session_id || sessionId
      if (!sessionId && responseSessionId) {
        setCurrentSessionId(responseSessionId)
      }

      // Create session info for parent component if this is a new session
      if (!sessionId && responseSessionId) {
        const newSession = {
          session_id: responseSessionId,
          title: userMessage.content.slice(0, 50) + (userMessage.content.length > 50 ? '...' : ''),
          created_at: new Date().toISOString(),
          last_activity: new Date().toISOString(),
          status: 'processing'
        }
        onSessionCreated(newSession)
      }

      // Show progress logger for processing requests
      if (response.status === 'processing') {
        setShowProgressLogger(true)
      } else {
        // Add assistant response for immediate responses
        const assistantMessage = {
          type: 'assistant',
          content: response.response_content || 'Processing your request...',
          timestamp: new Date().toISOString(),
          chart_data: response.chart_data,
          file_info: response.file_info,
          progress: response.progress
        }
        setMessages(prev => [...prev, assistantMessage])
      }

    } catch (error) {
      console.error('Failed to send message:', error)
      
      const errorMessage = {
        type: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString()
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleExampleClick = (exampleQuery) => {
    setInputValue(exampleQuery)
    // Optional: Auto-submit the example query
    setTimeout(() => {
      const fakeEvent = { preventDefault: () => {} }
      setInputValue(exampleQuery)
      setTimeout(() => {
        handleSubmit(fakeEvent)
      }, 100)
    }, 100)
  }

  const handleFileUpload = (fileInfo) => {
    const fileMessage = {
      type: 'user',
      content: `Uploaded file: ${fileInfo.filename}`,
      timestamp: new Date().toISOString(),
      file_info: fileInfo
    }
    setMessages(prev => [...prev, fileMessage])
    setShowFileUpload(false)
  }

  const handleProgressComplete = async () => {
    // Hide progress logger
    setShowProgressLogger(false)
    
    // Reload session to get the final response
    if (currentSessionId) {
      try {
        await loadSession()
      } catch (error) {
        console.error('Failed to reload session after completion:', error)
      }
    }
  }

  return (
    <div className="flex-1 flex flex-col h-full bg-white">
      {/* Chat Header */}
      <div className="border-b border-gray-200 p-4 bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-medium text-gray-900">
              {sessionId ? 'Chat Session' : 'New Chat'}
            </h2>
            <p className="text-sm text-gray-500">
              Ask questions about your data or request visualizations
            </p>
          </div>
          {sessionId && (
            <div className="text-xs text-gray-400">
              Session ID: {sessionId.slice(0, 8)}...
            </div>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList 
          messages={messages} 
          isLoading={isLoading} 
          onExampleClick={handleExampleClick}
        />
        
        {/* Progress Logger */}
        <ProgressLogger
          sessionId={currentSessionId}
          isVisible={showProgressLogger}
          onComplete={handleProgressComplete}
        />
      </div>

      {/* File Upload Modal */}
      {showFileUpload && (
        <FileUpload
          onFileUploaded={handleFileUpload}
          onClose={() => setShowFileUpload(false)}
        />
      )}

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <button
            type="button"
            onClick={() => setShowFileUpload(true)}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Paperclip size={20} />
          </button>
          
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message here..."
              disabled={isLoading}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent disabled:bg-gray-100"
            />
          </div>
          
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            <Send size={16} />
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
        
        <div className="mt-2 text-xs text-gray-500">
          Try: "bar chart" • "Excel spreadsheet" • "analyze insights" • "processing status"
        </div>
      </div>
    </div>
  )
}

export default ChatArea 