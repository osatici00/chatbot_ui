import React, { useState, useEffect, useRef } from 'react'
import { Clock, CheckCircle, XCircle, Loader2 } from 'lucide-react'

function ProgressLogger({ sessionId, isVisible, onComplete }) {
  const [logs, setLogs] = useState([])
  const [isConnected, setIsConnected] = useState(false)
  const [connectionError, setConnectionError] = useState(null)
  const wsRef = useRef(null)
  const logsEndRef = useRef(null)

  useEffect(() => {
    if (!sessionId || !isVisible) return

    // Connect to WebSocket for real-time progress updates
    const connectWebSocket = () => {
      try {
        const wsUrl = `ws://localhost:8001/ws/progress/${sessionId}`
        wsRef.current = new WebSocket(wsUrl)

        wsRef.current.onopen = () => {
          console.log('Progress WebSocket connected')
          setIsConnected(true)
          setConnectionError(null)
        }

        wsRef.current.onmessage = (event) => {
          try {
            const logEntry = JSON.parse(event.data)
            setLogs(prevLogs => {
              // Avoid duplicates based on timestamp and step
              const exists = prevLogs.some(log => 
                log.timestamp === logEntry.timestamp && log.step === logEntry.step
              )
              if (exists) return prevLogs
              
              const newLogs = [...prevLogs, logEntry]
              
              // Check if processing is complete
              if (logEntry.step === 'Finished' || logEntry.step === 'Completed') {
                setTimeout(() => {
                  onComplete && onComplete()
                }, 2000) // Show completion for 2 seconds before calling onComplete
              }
              
              return newLogs
            })
          } catch (error) {
            console.error('Error parsing WebSocket message:', error)
          }
        }

        wsRef.current.onclose = () => {
          console.log('Progress WebSocket disconnected')
          setIsConnected(false)
        }

        wsRef.current.onerror = (error) => {
          console.error('WebSocket error:', error)
          setConnectionError('Connection failed')
          setIsConnected(false)
        }
      } catch (error) {
        console.error('Failed to create WebSocket:', error)
        setConnectionError('Failed to connect')
      }
    }

    connectWebSocket()

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [sessionId, isVisible, onComplete])

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs])

  const getStepIcon = (step, stepNumber, totalSteps) => {
    if (step === 'Error') {
      return <XCircle className="text-red-500" size={16} />
    } else if (step === 'Finished' || step === 'Completed') {
      return <CheckCircle className="text-green-500" size={16} />
    } else if (step === 'Starting') {
      return <Loader2 className="text-blue-500 animate-spin" size={16} />
    } else {
      return <Loader2 className="text-blue-500 animate-spin" size={16} />
    }
  }

  const getProgressPercentage = (stepNumber, totalSteps) => {
    if (!stepNumber || !totalSteps) return 0
    return Math.round((stepNumber / totalSteps) * 100)
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    })
  }

  if (!isVisible) return null

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 m-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-gray-700 flex items-center gap-2">
          <Loader2 className="animate-spin" size={16} />
          Processing Analysis
        </h3>
        <div className="flex items-center gap-2">
          {connectionError && (
            <span className="text-xs text-red-500">{connectionError}</span>
          )}
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-gray-400'}`} />
          <span className="text-xs text-gray-500">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      <div className="space-y-2 max-h-64 overflow-y-auto">
        {logs.length === 0 ? (
          <div className="text-sm text-gray-500 italic">
            Waiting for progress updates...
          </div>
        ) : (
          logs.map((log, index) => (
            <div
              key={`${log.timestamp}-${index}`}
              className={`flex items-start gap-3 p-2 rounded transition-all duration-300 ${
                log.step === 'Error' 
                  ? 'bg-red-50 border-l-2 border-red-400' 
                  : log.step === 'Finished' || log.step === 'Completed'
                  ? 'bg-green-50 border-l-2 border-green-400'
                  : 'bg-white border-l-2 border-blue-400'
              }`}
              style={{
                animation: `slideIn 0.3s ease-out ${index * 0.1}s both`
              }}
            >
              <div className="flex-shrink-0 mt-0.5">
                {getStepIcon(log.step, log.step_number, log.total_steps)}
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-gray-900">
                    {log.step}
                  </span>
                  <span className="text-xs text-gray-500 flex items-center gap-1">
                    <Clock size={12} />
                    {formatTime(log.timestamp)}
                  </span>
                </div>
                
                <p className="text-sm text-gray-600 mb-2">
                  {log.message}
                </p>
                
                {log.step_number && log.total_steps && (
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-1.5">
                      <div
                        className="bg-blue-500 h-1.5 rounded-full transition-all duration-500"
                        style={{
                          width: `${getProgressPercentage(log.step_number, log.total_steps)}%`
                        }}
                      />
                    </div>
                    <span className="text-xs text-gray-500">
                      {log.step_number}/{log.total_steps}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={logsEndRef} />
      </div>

      {logs.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Real-time progress updates</span>
            <span>{logs.length} steps logged</span>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  )
}

export default ProgressLogger 