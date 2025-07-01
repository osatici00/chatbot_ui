import React from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Bar, Line, Pie, Scatter } from 'react-chartjs-2'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

function ChartDisplay({ chartData }) {
  if (!chartData || !chartData.type) {
    return null
  }

  const { type, data, options, title } = chartData

  // Common chart options
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top'
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        cornerRadius: 8,
        displayColors: true
      }
    },
    ...options
  }

  const renderChart = () => {
    switch (type) {
      case 'bar':
        return <Bar data={data} options={defaultOptions} />
      
      case 'line':
        return <Line data={data} options={defaultOptions} />
      
      case 'pie':
        return <Pie data={data} options={defaultOptions} />
      
      case 'scatter':
        return <Scatter data={data} options={defaultOptions} />
      
      default:
        return (
          <div className="text-center py-8 text-gray-500">
            Unsupported chart type: {type}
          </div>
        )
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 my-4">
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
          {title}
        </h3>
      )}
      <div className="relative h-80 w-full">
        {renderChart()}
      </div>
      <div className="mt-4 text-xs text-gray-500 text-center">
        Interactive chart - hover for details, click legend to toggle data series
      </div>
    </div>
  )
}

export default ChartDisplay 