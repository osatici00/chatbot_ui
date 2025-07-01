import React, { useState } from 'react'
import { Bot, Download, Copy, CheckCircle, FileText, BarChart3 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import ChartDisplay from './ChartDisplay'

function AssistantMessage({ message }) {
  const [copied, setCopied] = useState(false)

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy:', error)
    }
  }

  const getFileIcon = (fileType) => {
    switch (fileType) {
      case 'excel':
        return <BarChart3 size={16} className="text-green-600" />
      case 'pdf':
        return <FileText size={16} className="text-red-600" />
      default:
        return <Download size={16} className="text-blue-600" />
    }
  }

  const handleDownload = (fileInfo) => {
    // In a real app, this would trigger actual download
    alert(`Downloading ${fileInfo.filename}...`)
  }

  return (
    <div className="flex justify-start message-fade-in">
      <div className="max-w-4xl bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
            <Bot size={16} className="text-white" />
          </div>
          <div className="flex-1 min-w-0">
            {/* Progress indicator */}
            {message.progress && (
              <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-blue-900">
                    {message.progress.current_step}
                  </span>
                  <span className="text-sm text-blue-700">
                    {message.progress.percentage}%
                  </span>
                </div>
                <div className="w-full bg-blue-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${message.progress.percentage}%` }}
                  ></div>
                </div>
                <p className="text-xs text-blue-700 mt-1">
                  Step {message.progress.total_steps - 1} of {message.progress.total_steps}
                </p>
              </div>
            )}

            {/* Interactive Chart Display */}
            {message.chart_data && (
              <ChartDisplay chartData={message.chart_data} />
            )}

            {/* Main content */}
            <div className="prose prose-sm max-w-none">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>

            {/* File download */}
            {message.file_info && (
              <div className="mt-4 p-3 bg-white border border-gray-200 rounded">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {getFileIcon(message.file_info.file_type)}
                    <div>
                      <p className="font-medium text-sm text-gray-900">
                        {message.file_info.filename}
                      </p>
                      <p className="text-xs text-gray-500">
                        {message.file_info.file_size}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDownload(message.file_info)}
                    className="flex items-center gap-2 px-3 py-2 bg-primary text-white text-sm rounded hover:bg-blue-600 transition-colors"
                  >
                    <Download size={14} />
                    Download
                  </button>
                </div>
              </div>
            )}

            {/* Footer with timestamp and copy button */}
            <div className="flex items-center justify-between mt-3 pt-2 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                {formatTime(message.timestamp)}
              </p>
              <button
                onClick={copyToClipboard}
                className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors"
              >
                {copied ? (
                  <>
                    <CheckCircle size={12} className="text-green-500" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy size={12} />
                    Copy
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AssistantMessage 