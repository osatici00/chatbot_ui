import React from 'react'
import { User, FileText, FileSpreadsheet, File } from 'lucide-react'

function UserMessage({ message }) {
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getFileIcon = (filename) => {
    const extension = filename.split('.').pop()?.toLowerCase()
    
    switch (extension) {
      case 'pdf':
        return <FileText size={16} className="text-red-500" />
      case 'xlsx':
      case 'xls':
      case 'csv':
        return <FileSpreadsheet size={16} className="text-green-500" />
      default:
        return <File size={16} className="text-blue-500" />
    }
  }

  return (
    <div className="flex justify-end message-fade-in">
      <div className="max-w-4xl bg-primary text-white rounded-lg p-4">
        <div className="flex items-start gap-3">
          <div className="flex-1 min-w-0">
            <p className="text-white">{message.content}</p>
            
            {/* File attachment display */}
            {message.file_info && (
              <div className="mt-3 p-2 bg-blue-600 rounded border border-blue-500">
                <div className="flex items-center gap-2">
                  {getFileIcon(message.file_info.filename)}
                  <div>
                    <p className="text-sm font-medium">
                      {message.file_info.filename}
                    </p>
                    <p className="text-xs text-blue-200">
                      File uploaded successfully
                    </p>
                  </div>
                </div>
              </div>
            )}
            
            <div className="flex items-center justify-between mt-2 pt-2 border-t border-blue-400">
              <div></div>
              <p className="text-xs text-blue-200">
                {formatTime(message.timestamp)}
              </p>
            </div>
          </div>
          <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center flex-shrink-0">
            <User size={16} className="text-primary" />
          </div>
        </div>
      </div>
    </div>
  )
}

export default UserMessage 