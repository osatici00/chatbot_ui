import React, { useEffect, useRef } from 'react'
import UserMessage from './UserMessage'
import AssistantMessage from './AssistantMessage'
import LoadingMessage from './LoadingMessage'

function MessageList({ messages, isLoading, onExampleClick }) {
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  const handleExampleClick = (exampleQuery) => {
    if (onExampleClick) {
      onExampleClick(exampleQuery)
    }
  }

  return (
    <div className="h-full overflow-y-auto p-4 space-y-4">
      {messages.length === 0 && !isLoading && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">💬</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Start a new conversation
          </h2>
          <p className="text-gray-500 max-w-md mx-auto">
            Ask questions about your data, request visualizations, or upload files for analysis.
          </p>
          <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 max-w-6xl mx-auto">
            {/* Chart Examples - User's exact queries */}
            <div 
              className="p-3 bg-blue-50 rounded-lg border border-blue-200 cursor-pointer hover:bg-blue-100 transition-colors"
              onClick={() => handleExampleClick("Show me a revenue chart by region")}
            >
              <h4 className="font-medium text-sm text-blue-900 mb-1">📊 Bar Chart</h4>
              <p className="text-xs text-blue-700">"Show me a revenue chart by region"</p>
            </div>
            
            <div 
              className="p-3 bg-green-50 rounded-lg border border-green-200 cursor-pointer hover:bg-green-100 transition-colors"
              onClick={() => handleExampleClick("Create a customer satisfaction trend line")}
            >
              <h4 className="font-medium text-sm text-green-900 mb-1">📈 Line Chart</h4>
              <p className="text-xs text-green-700">"Create a customer satisfaction trend line"</p>
            </div>
            
            <div 
              className="p-3 bg-purple-50 rounded-lg border border-purple-200 cursor-pointer hover:bg-purple-100 transition-colors"
              onClick={() => handleExampleClick("Display support ticket distribution pie chart")}
            >
              <h4 className="font-medium text-sm text-purple-900 mb-1">🥧 Pie Chart</h4>
              <p className="text-xs text-purple-700">"Display support ticket distribution pie chart"</p>
            </div>
            
            <div 
              className="p-3 bg-orange-50 rounded-lg border border-orange-200 cursor-pointer hover:bg-orange-100 transition-colors"
              onClick={() => handleExampleClick("Generate a scatter plot of order value vs satisfaction")}
            >
              <h4 className="font-medium text-sm text-orange-900 mb-1">⚫ Scatter Plot</h4>
              <p className="text-xs text-orange-700">"Generate a scatter plot of order value vs satisfaction"</p>
            </div>

            {/* Other Response Types */}
            <div 
              className="p-3 bg-emerald-50 rounded-lg border border-emerald-200 cursor-pointer hover:bg-emerald-100 transition-colors"
              onClick={() => handleExampleClick("Analyze customer insights and provide summary")}
            >
              <h4 className="font-medium text-sm text-emerald-900 mb-1">📄 Text Analysis</h4>
              <p className="text-xs text-emerald-700">"Analyze customer insights and provide summary"</p>
            </div>
            
            <div 
              className="p-3 bg-indigo-50 rounded-lg border border-indigo-200 cursor-pointer hover:bg-indigo-100 transition-colors"
              onClick={() => handleExampleClick("Export sales data to Excel spreadsheet")}
            >
              <h4 className="font-medium text-sm text-indigo-900 mb-1">📥 Excel Download</h4>
              <p className="text-xs text-indigo-700">"Export sales data to Excel spreadsheet"</p>
            </div>
            
            <div 
              className="p-3 bg-yellow-50 rounded-lg border border-yellow-200 cursor-pointer hover:bg-yellow-100 transition-colors"
              onClick={() => handleExampleClick("Check processing status of my request")}
            >
              <h4 className="font-medium text-sm text-yellow-900 mb-1">⏳ Progress Status</h4>
              <p className="text-xs text-yellow-700">"Check processing status of my request"</p>
            </div>
          </div>
        </div>
      )}

      {messages.map((message, index) => (
        <div key={index}>
          {message.type === 'user' ? (
            <UserMessage message={message} />
          ) : (
            <AssistantMessage message={message} />
          )}
        </div>
      ))}

      {isLoading && <LoadingMessage />}
      
      <div ref={messagesEndRef} />
    </div>
  )
}

export default MessageList 