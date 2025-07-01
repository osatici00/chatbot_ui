import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 404) {
      console.error('API endpoint not found:', error.config.url)
    } else if (error.response?.status >= 500) {
      console.error('Server error:', error.response.data)
    }
    return Promise.reject(error)
  }
)

export const sendQuery = async (userQuery, userEmail, sessionId = null) => {
  try {
    const response = await api.post('/query', {
      user_query: userQuery,
      user_email: userEmail,
      session_id: sessionId
    })
    return response.data
  } catch (error) {
    console.error('Failed to send query:', error)
    throw error
  }
}

export const getSessions = async () => {
  try {
    const response = await api.get('/sessions')
    return response.data
  } catch (error) {
    console.error('Failed to get sessions:', error)
    throw error
  }
}

export const getSession = async (sessionId) => {
  try {
    const response = await api.get(`/sessions/${sessionId}`)
    return response.data
  } catch (error) {
    console.error('Failed to get session:', error)
    throw error
  }
}

export const deleteSession = async (sessionId) => {
  try {
    const response = await api.delete(`/sessions/${sessionId}`)
    return response.data
  } catch (error) {
    console.error('Failed to delete session:', error)
    throw error
  }
}

export const uploadFile = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  } catch (error) {
    console.error('Failed to upload file:', error)
    throw error
  }
}

export const getProgress = async (sessionId) => {
  try {
    const response = await api.get(`/progress/${sessionId}`)
    return response.data
  } catch (error) {
    console.error('Failed to get progress:', error)
    throw error
  }
}

export const markNotificationRead = async (sessionId) => {
  try {
    const response = await api.post(`/sessions/${sessionId}/mark-read`)
    return response.data
  } catch (error) {
    console.error('Failed to mark notification as read:', error)
    throw error
  }
}

export default api 