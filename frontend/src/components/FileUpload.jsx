import React, { useState, useRef } from 'react'
import { Upload, X, File, CheckCircle } from 'lucide-react'
import { uploadFile } from '../services/api'

function FileUpload({ onFileUploaded, onClose }) {
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadSuccess, setUploadSuccess] = useState(false)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    
    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      handleFileUpload(files[0])
    }
  }

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    if (files.length > 0) {
      handleFileUpload(files[0])
    }
  }

  const handleFileUpload = async (file) => {
    // Validate file type
    const allowedTypes = [
      'text/csv',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/pdf'
    ]

    if (!allowedTypes.includes(file.type)) {
      alert('Please upload a CSV, Excel, or PDF file.')
      return
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB.')
      return
    }

    setIsUploading(true)

    try {
      const response = await uploadFile(file)
      setUploadSuccess(true)
      
      setTimeout(() => {
        onFileUploaded({
          filename: file.name,
          file_size: `${(file.size / 1024).toFixed(1)} KB`,
          file_type: file.type,
          ...response
        })
      }, 1000)

    } catch (error) {
      console.error('Upload failed:', error)
      alert('Upload failed. Please try again.')
      setIsUploading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Upload File</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X size={20} />
          </button>
        </div>

        {!uploadSuccess ? (
          <>
            <div
              className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                isDragging
                  ? 'border-primary bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              {isUploading ? (
                <div>
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                  <p className="text-gray-600">Uploading...</p>
                </div>
              ) : (
                <>
                  <Upload size={48} className="mx-auto mb-4 text-gray-400" />
                  <p className="text-gray-600 mb-2">
                    Drag and drop your file here, or{' '}
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="text-primary hover:underline"
                    >
                      browse
                    </button>
                  </p>
                  <p className="text-sm text-gray-500">
                    Supports CSV, Excel, and PDF files (max 10MB)
                  </p>
                </>
              )}
            </div>

            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileSelect}
              accept=".csv,.xlsx,.xls,.pdf"
              className="hidden"
            />

            <div className="mt-4">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Supported file types:</h4>
              <div className="space-y-1 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <File size={14} />
                  <span>CSV files (.csv)</span>
                </div>
                <div className="flex items-center gap-2">
                  <File size={14} />
                  <span>Excel files (.xlsx, .xls)</span>
                </div>
                <div className="flex items-center gap-2">
                  <File size={14} />
                  <span>PDF documents (.pdf)</span>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="text-center py-8">
            <CheckCircle size={48} className="mx-auto mb-4 text-green-500" />
            <h4 className="text-lg font-semibold text-gray-900 mb-2">
              Upload Successful!
            </h4>
            <p className="text-gray-600">
              Your file has been uploaded and is ready for analysis.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default FileUpload 