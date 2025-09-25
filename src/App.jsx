import React, { useState } from 'react'
import AgentDashboard from './components/AgentDashboard'
import AIAssistant from './components/AIAssistant'
import Calendar from './components/Calendar'
import LeadDashboard from './components/LeadDashboard'
import RealTimeAnalytics from './components/RealTimeAnalytics'
import StrategyAI from './components/StrategyAI'
import SocialMedia from './components/SocialMedia'
import {
  Brain,
  Activity,
  Calendar as CalendarIcon,
  BarChart3,
  TrendingUp,
  Bot,
  Menu,
  X,
  Send
} from 'lucide-react'

function App() {
  const [activeTab, setActiveTab] = useState('strategy')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const tabs = [
    {
      id: 'strategy',
      name: 'Strategy AI',
      icon: <Bot className="w-5 h-5" />,
      component: StrategyAI
    },
    {
      id: 'agents',
      name: 'Agent Dashboard',
      icon: <Brain className="w-5 h-5" />,
      component: AgentDashboard
    },
    {
      id: 'social',
      name: 'Social Media',
      icon: <Send className="w-5 h-5" />,
      component: SocialMedia
    },
    {
      id: 'leads',
      name: 'Lead Dashboard',
      icon: <TrendingUp className="w-5 h-5" />,
      component: LeadDashboard
    },
    {
      id: 'calendar',
      name: 'Calendar',
      icon: <CalendarIcon className="w-5 h-5" />,
      component: Calendar
    },
    {
      id: 'analytics',
      name: 'Analytics',
      icon: <BarChart3 className="w-5 h-5" />,
      component: RealTimeAnalytics
    }
  ]

  const ActiveComponent = tabs.find(tab => tab.id === activeTab)?.component || StrategyAI

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="md:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
              >
                {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
              <div className="flex items-center ml-4 md:ml-0">
                <Brain className="w-8 h-8 text-blue-600" />
                <h1 className="ml-3 text-xl font-semibold text-gray-900">
                  AI Lead Generation Agent
                </h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                <Activity className="w-4 h-4" />
                <span>System Online</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out md:translate-x-0 md:static md:inset-0`}>
          <div className="flex flex-col h-full">
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">Navigation</h2>
              <button
                onClick={() => setSidebarOpen(false)}
                className="md:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <nav className="flex-1 px-4 py-6 space-y-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id)
                    setSidebarOpen(false)
                  }}
                  className={`w-full flex items-center px-4 py-3 text-left rounded-lg transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-100 text-blue-700 border-r-4 border-blue-600'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                >
                  {tab.icon}
                  <span className="ml-3 font-medium">{tab.name}</span>
                </button>
              ))}
            </nav>
            <div className="p-4 border-t border-gray-200">
              <div className="text-xs text-gray-500">
                <p className="mb-2">🤖 Autonomous Lead Generation</p>
                <p>24/7 AI-powered business growth</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 md:ml-0">
          <main className="p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {tabs.find(tab => tab.id === activeTab)?.name || 'Dashboard'}
              </h2>
              <p className="mt-1 text-gray-600">
                {activeTab === 'strategy' && 'Chat with your AI business strategist'}
                {activeTab === 'agents' && 'Monitor your autonomous AI agents'}
                {activeTab === 'social' && 'Create and post content with AI assistance'}
                {activeTab === 'leads' && 'Track and manage your leads'}
                {activeTab === 'calendar' && 'Plan your schedule with AI assistance'}
                {activeTab === 'analytics' && 'View real-time performance metrics'}
              </p>
            </div>

            <div className="bg-white rounded-lg shadow">
              <ActiveComponent />
            </div>
          </main>
        </div>
      </div>

      {/* Overlay for mobile sidebar */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-25 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}

export default App
