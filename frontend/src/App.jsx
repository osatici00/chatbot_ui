import React, { useState } from 'react'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import './styles/index.css'

function App() {
  const [selectedSessionId, setSelectedSessionId] = useState(null)
  const [sessions, setSessions] = useState([])

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

  return (
    <div className="flex h-screen bg-gray-100">
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
  )
}

export default App 