import React, { useState, useEffect } from 'react'
import { Plus, Search, Trash2, MessageCircle } from 'lucide-react'
import { getSessions, deleteSession } from '../services/api'

function Sidebar({ 
  sessions, 
  selectedSessionId, 
  onSessionSelect, 
  onSessionDeleted, 
  onNewChat, 
  setSessions 
}) {
  const [searchTerm, setSearchTerm] = useState('')
  const [filteredSessions, setFilteredSessions] = useState([])

  // Load sessions on component mount
  useEffect(() => {
    loadSessions()
  }, [])

  // Filter sessions based on search term
  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredSessions(sessions)
    } else {
      const filtered = sessions.filter(session =>
        session.title.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredSessions(filtered)
    }
  }, [sessions, searchTerm])

  const loadSessions = async () => {
    try {
      const data = await getSessions()
      setSessions(data)
    } catch (error) {
      console.error('Failed to load sessions:', error)
    }
  }

  const handleDeleteSession = async (sessionId) => {
    if (confirm('Are you sure you want to delete this session?')) {
      try {
        await deleteSession(sessionId)
        onSessionDeleted(sessionId)
      } catch (error) {
        console.error('Failed to delete session:', error)
      }
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = (now - date) / (1000 * 60 * 60)

    if (diffInHours < 24) {
      return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    } else {
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
      })
    }
  }

  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <button
          onClick={onNewChat}
          className="w-full flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          <Plus size={16} />
          New Chat
        </button>
      </div>

      {/* Search */}
      <div className="p-4">
        <div className="relative">
          <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search conversations..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          />
        </div>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto">
        {filteredSessions.length === 0 ? (
          <div className="p-4 text-center text-gray-500">
            {searchTerm ? 'No matching conversations' : 'No conversations yet'}
          </div>
        ) : (
          filteredSessions.map((session) => (
            <div
              key={session.session_id}
              className={`mx-2 mb-2 p-3 rounded-lg border cursor-pointer hover:bg-gray-50 transition-colors ${
                selectedSessionId === session.session_id
                  ? 'bg-blue-50 border-blue-200'
                  : 'bg-white border-gray-200'
              }`}
              onClick={() => onSessionSelect(session.session_id)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <MessageCircle size={14} className="text-gray-400 flex-shrink-0" />
                    <h3 className="font-medium text-sm text-gray-900 truncate">
                      {session.title}
                    </h3>
                  </div>
                  <p className="text-xs text-gray-500">
                    {formatDate(session.last_activity)}
                  </p>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    handleDeleteSession(session.session_id)
                  }}
                  className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 text-center">
          ChatGPT UI Demo v1.0
        </p>
      </div>
    </div>
  )
}

export default Sidebar 