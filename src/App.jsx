import React, { useState, useEffect } from 'react'
import Calendar from './components/Calendar'
import TimeBlock from './components/TimeBlock'
import AIAssistant from './components/AIAssistant'
import ScheduleModal from './components/ScheduleModal'
import LeadDashboard from './components/LeadDashboard'
import StrategyAI from './components/StrategyAI'
import AgentDashboard from './components/AgentDashboard'
import { generateTimeSlots, formatTime } from './utils/timeUtils'
import { getAISuggestions } from './services/aiService'
import { Calendar as CalendarIcon, Clock, Brain, Users, Target, Activity } from 'lucide-react'

function App() {
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [timeBlocks, setTimeBlocks] = useState({})
  const [showModal, setShowModal] = useState(false)
  const [editingBlock, setEditingBlock] = useState(null)
  const [aiSuggestions, setAiSuggestions] = useState([])
  const [isLoadingAI, setIsLoadingAI] = useState(false)
  const [activeTab, setActiveTab] = useState('strategy') // 'scheduler', 'leads', 'strategy', or 'agent'

  const timeSlots = generateTimeSlots()

  // Load saved time blocks from localStorage
  useEffect(() => {
    const savedBlocks = localStorage.getItem('timeBlocks')
    if (savedBlocks) {
      setTimeBlocks(JSON.parse(savedBlocks))
    }
  }, [])

  // Save time blocks to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('timeBlocks', JSON.stringify(timeBlocks))
  }, [timeBlocks])

  // Generate AI suggestions when date changes
  useEffect(() => {
    if (selectedDate) {
      generateAISuggestions()
    }
  }, [selectedDate, timeBlocks])

  const generateAISuggestions = async () => {
    setIsLoadingAI(true)
    try {
      const dateKey = selectedDate.toDateString()
      const dayBlocks = timeBlocks[dateKey] || []
      
      const suggestions = await getAISuggestions(selectedDate, dayBlocks)
      setAiSuggestions(suggestions)
    } catch (error) {
      console.error('Error generating AI suggestions:', error)
    } finally {
      setIsLoadingAI(false)
    }
  }

  const handleDateSelect = (date) => {
    setSelectedDate(date)
  }

  const handleTimeSlotClick = (timeSlot) => {
    setEditingBlock({
      date: selectedDate,
      startTime: timeSlot,
      endTime: timeSlot + 1,
      title: '',
      category: 'work',
      description: ''
    })
    setShowModal(true)
  }

  const handleSaveBlock = (blockData) => {
    const dateKey = blockData.date.toDateString()
    const newBlocks = { ...timeBlocks }
    
    if (!newBlocks[dateKey]) {
      newBlocks[dateKey] = []
    }

    if (editingBlock && editingBlock.id) {
      // Update existing block
      const blockIndex = newBlocks[dateKey].findIndex(b => b.id === editingBlock.id)
      if (blockIndex !== -1) {
        newBlocks[dateKey][blockIndex] = { ...blockData, id: editingBlock.id }
      }
    } else {
      // Add new block
      const newBlock = {
        ...blockData,
        id: Date.now() + Math.random()
      }
      newBlocks[dateKey].push(newBlock)
    }

    setTimeBlocks(newBlocks)
    setShowModal(false)
    setEditingBlock(null)
  }

  const handleDeleteBlock = (blockId) => {
    const dateKey = selectedDate.toDateString()
    const newBlocks = { ...timeBlocks }
    
    if (newBlocks[dateKey]) {
      newBlocks[dateKey] = newBlocks[dateKey].filter(block => block.id !== blockId)
      setTimeBlocks(newBlocks)
    }
  }

  const handleEditBlock = (block) => {
    setEditingBlock(block)
    setShowModal(true)
  }

  const getBlocksForTimeSlot = (timeSlot) => {
    const dateKey = selectedDate.toDateString()
    const dayBlocks = timeBlocks[dateKey] || []
    
    return dayBlocks.filter(block => {
      const blockStart = parseInt(block.startTime)
      const blockEnd = parseInt(block.endTime)
      return timeSlot >= blockStart && timeSlot < blockEnd
    })
  }

  const applyAISuggestion = (suggestion) => {
    const dateKey = selectedDate.toDateString()
    const newBlocks = { ...timeBlocks }
    
    if (!newBlocks[dateKey]) {
      newBlocks[dateKey] = []
    }

    // Add suggested blocks
    suggestion.blocks.forEach(block => {
      const newBlock = {
        ...block,
        id: Date.now() + Math.random()
      }
      newBlocks[dateKey].push(newBlock)
    })

    setTimeBlocks(newBlocks)
  }

  return (
    <div className="container">
      <header className="card glass-effect">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Target size={32} color="#667eea" />
              <h1 style={{ fontSize: '28px', fontWeight: '700', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                AI Lead Generator
              </h1>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#64748b' }}>
              <Users size={20} />
              <span style={{ fontSize: '14px', fontWeight: '500' }}>
                Autonomous Lead Generation
              </span>
            </div>
          </div>
          
          {/* Tab Navigation */}
          <div style={{ display: 'flex', gap: '8px' }}>
            <button 
              className={`btn ${activeTab === 'strategy' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveTab('strategy')}
            >
              <Brain size={16} />
              Strategy AI
            </button>
            <button 
              className={`btn ${activeTab === 'agent' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveTab('agent')}
            >
              <Activity size={16} />
              Agent Tasks
            </button>
            <button 
              className={`btn ${activeTab === 'leads' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveTab('leads')}
            >
              <Users size={16} />
              Leads
            </button>
            <button 
              className={`btn ${activeTab === 'scheduler' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveTab('scheduler')}
            >
              <CalendarIcon size={16} />
              Scheduler
            </button>
          </div>
        </div>
      </header>

      {activeTab === 'strategy' ? (
        <div className="h-screen">
          <StrategyAI />
        </div>
      ) : activeTab === 'agent' ? (
        <AgentDashboard />
      ) : activeTab === 'leads' ? (
        <LeadDashboard />
      ) : (
        <>
          <div className="calendar-container">
            <div className="card">
              <h2 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CalendarIcon size={20} />
                Calendar
              </h2>
              <Calendar 
                selectedDate={selectedDate}
                onDateSelect={handleDateSelect}
                timeBlocks={timeBlocks}
              />
            </div>

            <div className="card">
              <h2 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Clock size={20} />
                Daily Schedule
              </h2>
              <TimeBlock
                selectedDate={selectedDate}
                timeSlots={timeSlots}
                timeBlocks={timeBlocks}
                onTimeSlotClick={handleTimeSlotClick}
                onEditBlock={handleEditBlock}
                onDeleteBlock={handleDeleteBlock}
              />
            </div>
          </div>

          <div className="card">
            <h2 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Brain size={20} />
              AI Assistant
            </h2>
            <AIAssistant
              selectedDate={selectedDate}
              suggestions={aiSuggestions}
              onApplySuggestion={applyAISuggestion}
              isLoading={isLoadingAI}
            />
          </div>
        </>
      )}

      {showModal && (
        <ScheduleModal
          isOpen={showModal}
          onClose={() => {
            setShowModal(false)
            setEditingBlock(null)
          }}
          onSave={handleSaveBlock}
          initialData={editingBlock}
          selectedDate={selectedDate}
        />
      )}
    </div>
  )
}

export default App
