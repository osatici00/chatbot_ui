import React from 'react'
import { Brain, Plus } from 'lucide-react'

function Header({ onNewChat }) {
  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div 
          className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
          onClick={onNewChat}
        >
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Brain size={20} className="text-white" />
          </div>
          <h1 className="text-xl font-semibold text-gray-900">
            Intelligent Assistant
          </h1>
        </div>
        
        <button
          onClick={onNewChat}
          className="flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus size={16} />
          New Chat
        </button>
      </div>
    </div>
  )
}

export default Header 