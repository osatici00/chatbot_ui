import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import { getSessions } from './services/api'
import './styles/index.css'

function App() {
  const [selectedSessionId, setSelectedSessionId] = useState(null)
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)

  // Load sessions on app start
  useEffect(() => {
    loadInitialSessions()
  }, [])

  const loadInitialSessions = async () => {
    try {
      const data = await getSessions()
      setSessions(data)
      
      // Auto-select the most recent session if available
      if (data.length > 0 && !selectedSessionId) {
        setSelectedSessionId(data[0].session_id)
      }
    } catch (error) {
      console.error('Failed to load sessions on startup:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSessionSelect = (sessionId) => {
    setSelectedSessionId(sessionId)
  }

  const handleSessionCreated = (newSession) => {
    setSessions(prev => [newSession, ...prev])
    setSelectedSessionId(newSession.session_id)
  }

  const handleSessionDeleted = (sessionId) => {
    setSessions(prev => prev.filter(s => s.session_id !== sessionId))
    if (selectedSessionId === sessionId) {
      setSelectedSessionId(null)
    }
  }

  const handleNewChat = () => {
    setSelectedSessionId(null)
  }

  if (loading) {
    return (
      <div className="flex h-screen bg-gray-100 items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading sessions...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Header onNewChat={handleNewChat} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          sessions={sessions}
          selectedSessionId={selectedSessionId}
          onSessionSelect={handleSessionSelect}
          onSessionDeleted={handleSessionDeleted}
          onNewChat={handleNewChat}
          setSessions={setSessions}
        />
        <ChatArea
          sessionId={selectedSessionId}
          onSessionCreated={handleSessionCreated}
        />
      </div>
    </div>
  )
}

export default App 