import React, { useState, useEffect, useRef } from 'react'
import { Loader2, Clock, CheckCircle, XCircle } from 'lucide-react'

function ProgressMessage({ sessionId, onComplete }) {
  const [logs, setLogs] = useState([])
  const [isConnected, setIsConnected] = useState(false)
  const [currentStep, setCurrentStep] = useState('')
  const [isComplete, setIsComplete] = useState(false)
  const wsRef = useRef(null)

  useEffect(() => {
    if (!sessionId) return

    // Connect to WebSocket for real-time progress updates
    const connectWebSocket = () => {
      try {
        const wsUrl = `ws://localhost:8001/ws/progress/${sessionId}`
        wsRef.current = new WebSocket(wsUrl)

        wsRef.current.onopen = () => {
          console.log('Progress WebSocket connected')
          setIsConnected(true)
        }

        wsRef.current.onmessage = (event) => {
          try {
            const logEntry = JSON.parse(event.data)
            
            setLogs(prevLogs => {
              // Avoid duplicates
              const exists = prevLogs.some(log => 
                log.timestamp === logEntry.timestamp && log.step === logEntry.step
              )
              if (exists) return prevLogs
              
              const newLogs = [...prevLogs, logEntry]
              return newLogs
            })

            // Update current step
            setCurrentStep(logEntry.step)
            
            // Check if processing is complete
            if (logEntry.step === 'Finished' || logEntry.step === 'Completed') {
              setIsComplete(true)
              setTimeout(() => {
                onComplete && onComplete()
              }, 1000) // Wait 1 second to show completion before calling onComplete
            }
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
          setIsConnected(false)
        }
      } catch (error) {
        console.error('Failed to create WebSocket:', error)
      }
    }

    connectWebSocket()

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [sessionId, onComplete])

  const getStepIcon = (step) => {
    if (step === 'Error') {
      return <XCircle className="text-red-500" size={16} />
    } else if (step === 'Finished' || step === 'Completed') {
      return <CheckCircle className="text-green-500" size={16} />
    } else {
      return <Loader2 className="text-blue-500 animate-spin" size={16} />
    }
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

  const getProgressPercentage = () => {
    if (logs.length === 0) return 0
    const latestLog = logs[logs.length - 1]
    if (!latestLog.step_number || !latestLog.total_steps) return 0
    return Math.round((latestLog.step_number / latestLog.total_steps) * 100)
  }

  if (isComplete) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
        <div className="flex items-center gap-2 text-green-700">
          <CheckCircle size={20} />
          <span className="font-medium">Analysis Complete!</span>
        </div>
        <p className="text-green-600 text-sm mt-1">
          Your response is ready and will appear below shortly.
        </p>
      </div>
    )
  }

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Loader2 className="animate-spin text-blue-500" size={16} />
          <span className="font-medium text-blue-700">
            {currentStep || 'Processing your request...'}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-gray-400'}`} />
          <span className="text-xs text-gray-500">
            {getProgressPercentage()}%
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-3">
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-500 h-2 rounded-full transition-all duration-500"
            style={{ width: `${getProgressPercentage()}%` }}
          />
        </div>
      </div>

      {/* Recent Steps */}
      <div className="space-y-2 max-h-32 overflow-y-auto">
        {logs.slice(-3).map((log, index) => (
          <div key={`${log.timestamp}-${index}`} className="flex items-start gap-2 text-sm">
            <div className="flex-shrink-0 mt-0.5">
              {getStepIcon(log.step)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <span className="font-medium text-gray-900">
                  {log.step}
                </span>
                <span className="text-xs text-gray-500 flex items-center gap-1">
                  <Clock size={10} />
                  {formatTime(log.timestamp)}
                </span>
              </div>
              <p className="text-gray-600 text-xs">
                {log.message}
              </p>
            </div>
          </div>
        ))}
      </div>

      {logs.length === 0 && (
        <div className="text-sm text-gray-500 italic">
          Connecting to progress updates...
        </div>
      )}
    </div>
  )
}

export default ProgressMessage 