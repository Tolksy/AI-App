import React, { useState, useEffect } from 'react'
import { Activity, Clock, CheckCircle, XCircle, AlertCircle, Play, Pause, RefreshCw } from 'lucide-react'

const AgentDashboard = () => {
  const [activeTasks, setActiveTasks] = useState([])
  const [taskHistory, setTaskHistory] = useState([])
  const [taskStats, setTaskStats] = useState({})
  const [loading, setLoading] = useState(true)
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    fetchTaskData()
    
    if (autoRefresh) {
      const interval = setInterval(fetchTaskData, 5000) // Refresh every 5 seconds
      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  const fetchTaskData = async () => {
    try {
      const [activeResponse, historyResponse, statsResponse] = await Promise.all([
        fetch('http://localhost:8000/api/v1/agent/tasks/active'),
        fetch('http://localhost:8000/api/v1/agent/tasks/history?limit=20'),
        fetch('http://localhost:8000/api/v1/agent/tasks/stats')
      ])

      if (activeResponse.ok) {
        const activeData = await activeResponse.json()
        setActiveTasks(activeData.active_tasks || [])
      }

      if (historyResponse.ok) {
        const historyData = await historyResponse.json()
        setTaskHistory(historyData.task_history || [])
      }

      if (statsResponse.ok) {
        const statsData = await statsResponse.json()
        setTaskStats(statsData)
      }
    } catch (error) {
      console.error('Error fetching task data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'running':
        return <RefreshCw className="w-5 h-5 text-blue-500 animate-spin" />
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-500" />
      default:
        return <AlertCircle className="w-5 h-5 text-gray-500" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      case 'running':
        return 'bg-blue-100 text-blue-800'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'N/A'
    return new Date(timestamp).toLocaleString()
  }

  const formatTaskType = (taskType) => {
    return taskType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading agent tasks...</span>
      </div>
    )
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Agent Dashboard</h1>
            <p className="text-gray-600">Monitor your AI agent's real-time activities and performance</p>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                autoRefresh ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
              }`}
            >
              {autoRefresh ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              Auto Refresh {autoRefresh ? 'ON' : 'OFF'}
            </button>
            <button
              onClick={fetchTaskData}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <RefreshCw className="w-4 h-4" />
              Refresh Now
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Activity className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Tasks</p>
              <p className="text-2xl font-bold text-gray-900">{taskStats.active_tasks || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-gray-900">{taskStats.completed_tasks || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <XCircle className="w-6 h-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Failed</p>
              <p className="text-2xl font-bold text-gray-900">{taskStats.failed_tasks || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Activity className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Success Rate</p>
              <p className="text-2xl font-bold text-gray-900">{taskStats.success_rate || 0}%</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Active Tasks */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Active Tasks ({activeTasks.length})</h3>
          </div>
          <div className="p-6">
            {activeTasks.length === 0 ? (
              <div className="text-center py-8">
                <Activity className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">No active tasks</p>
                <p className="text-sm text-gray-400">Your agent is ready for new assignments</p>
              </div>
            ) : (
              <div className="space-y-4">
                {activeTasks.map((task) => (
                  <div key={task.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          {getStatusIcon(task.status)}
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(task.status)}`}>
                            {task.status}
                          </span>
                          <span className="text-xs text-gray-500">
                            {formatTaskType(task.task_type)}
                          </span>
                        </div>
                        <p className="text-sm font-medium text-gray-900 mb-1">{task.description}</p>
                        <p className="text-xs text-gray-500">
                          Started: {formatTimestamp(task.started_at)}
                        </p>
                        {task.progress_percentage > 0 && (
                          <div className="mt-2">
                            <div className="flex justify-between text-xs text-gray-600 mb-1">
                              <span>Progress</span>
                              <span>{task.progress_percentage}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${task.progress_percentage}%` }}
                              ></div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Task History */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Recent History ({taskHistory.length})</h3>
          </div>
          <div className="p-6">
            {taskHistory.length === 0 ? (
              <div className="text-center py-8">
                <Clock className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">No task history</p>
                <p className="text-sm text-gray-400">Completed tasks will appear here</p>
              </div>
            ) : (
              <div className="space-y-3">
                {taskHistory.map((task) => (
                  <div key={task.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
                    <div className="flex items-center gap-3">
                      {getStatusIcon(task.status)}
                      <div>
                        <p className="text-sm font-medium text-gray-900">{task.description}</p>
                        <p className="text-xs text-gray-500">
                          {formatTimestamp(task.completed_at || task.started_at)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(task.status)}`}>
                        {task.status}
                      </span>
                      <span className="text-xs text-gray-500">
                        {formatTaskType(task.task_type)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8 bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button
            onClick={async () => {
              try {
                const response = await fetch('http://localhost:8000/api/v1/agent/linkedin/search', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    search_query: 'AI software companies',
                    industry: 'technology',
                    company_size: '51-200'
                  })
                });
                if (response.ok) {
                  const result = await response.json();
                  console.log('LinkedIn search completed:', result);
                  fetchTaskData(); // Refresh the dashboard
                }
              } catch (error) {
                console.error('LinkedIn search error:', error);
              }
            }}
            className="flex items-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Activity className="w-5 h-5" />
            LinkedIn Search
          </button>
          <button
            onClick={async () => {
              try {
                const response = await fetch('http://localhost:8000/api/v1/agent/research/company', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    company_name: 'TechCorp Solutions',
                    industry: 'technology'
                  })
                });
                if (response.ok) {
                  const result = await response.json();
                  console.log('Company research completed:', result);
                  fetchTaskData();
                }
              } catch (error) {
                console.error('Company research error:', error);
              }
            }}
            className="flex items-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <RefreshCw className="w-5 h-5" />
            Research Company
          </button>
          <button
            onClick={async () => {
              try {
                const response = await fetch('http://localhost:8000/api/v1/agent/email/send', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    to_email: 'test@example.com',
                    company_name: 'TechCorp Solutions',
                    contact_name: 'John Doe',
                    industry: 'technology'
                  })
                });
                if (response.ok) {
                  const result = await response.json();
                  console.log('Email sent:', result);
                  fetchTaskData();
                }
              } catch (error) {
                console.error('Email sending error:', error);
              }
            }}
            className="flex items-center gap-2 px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            <CheckCircle className="w-5 h-5" />
            Send Email
          </button>
          <button
            onClick={async () => {
              try {
                const response = await fetch('http://localhost:8000/api/v1/agent/score-lead', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    lead_data: {
                      name: 'Jane Smith',
                      email: 'jane@techcorp.com',
                      company: 'TechCorp Solutions',
                      title: 'CTO',
                      industry: 'technology',
                      company_size: '51-200'
                    }
                  })
                });
                if (response.ok) {
                  const result = await response.json();
                  console.log('Lead scored:', result);
                  fetchTaskData();
                }
              } catch (error) {
                console.error('Lead scoring error:', error);
              }
            }}
            className="flex items-center gap-2 px-4 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
          >
            <Activity className="w-5 h-5" />
            Score Lead
          </button>
        </div>
      </div>
    </div>
  )
}

export default AgentDashboard
