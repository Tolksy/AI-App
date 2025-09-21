// AI Service for generating intelligent scheduling suggestions
// Integrates with RAG-based backend for advanced AI capabilities

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'

// Check if we're in production (deployed environment)
const isProduction = process.env.NODE_ENV === 'production' && !window.location.hostname.includes('localhost')

// Legacy patterns for fallback
const PRODUCTIVITY_PATTERNS = {
  morning: {
    bestHours: [9, 10, 11],
    categories: ['work', 'learning'],
    description: 'Peak focus hours for deep work'
  },
  afternoon: {
    bestHours: [14, 15, 16],
    categories: ['meeting', 'work'],
    description: 'Good for collaborative work and meetings'
  },
  evening: {
    bestHours: [19, 20, 21],
    categories: ['exercise', 'personal', 'learning'],
    description: 'Ideal for personal development and wellness'
  }
}

const BREAK_RECOMMENDATIONS = {
  short: { duration: 0.5, frequency: 'every 2 hours' },
  medium: { duration: 1, frequency: 'every 4 hours' },
  long: { duration: 1.5, frequency: 'lunch break' }
}

// Generate AI suggestions using RAG backend
export const getAISuggestions = async (selectedDate, existingBlocks) => {
  // Skip API call in production if no backend is configured
  if (isProduction && !process.env.REACT_APP_API_URL) {
    console.log('Production mode: Using fallback suggestions')
    return getFallbackSuggestions(existingBlocks)
  }

  try {
    // Try to use the new RAG backend
    const response = await fetch(`${API_BASE_URL}/scheduling/suggestions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        date: selectedDate.toISOString().split('T')[0],
        current_blocks: existingBlocks.map(block => ({
          id: block.id,
          title: block.title,
          category: block.category,
          start_time: block.startTime,
          end_time: block.endTime,
          description: block.description,
          date: selectedDate.toISOString().split('T')[0]
        })),
        goals: ['productivity', 'work_life_balance', 'efficiency']
      })
    })

    if (response.ok) {
      const data = await response.json()
      return data.map(suggestion => ({
        type: suggestion.type,
        title: suggestion.title,
        description: suggestion.description,
        blocks: suggestion.blocks.map(block => ({
          title: block.title,
          category: block.category,
          startTime: block.start_time,
          endTime: block.end_time,
          description: block.description
        })),
        reasons: suggestion.reasons
      }))
    } else {
      console.warn('RAG backend unavailable, using fallback suggestions')
      return getFallbackSuggestions(existingBlocks)
    }
  } catch (error) {
    console.warn('Error connecting to RAG backend, using fallback:', error)
    return getFallbackSuggestions(existingBlocks)
  }
}

// Fallback to original logic if backend is unavailable
const getFallbackSuggestions = async (existingBlocks) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  const suggestions = []
  const currentHour = new Date().getHours()
  
  // Analyze existing blocks
  const analysis = analyzeSchedule(existingBlocks)
  
  // 1. Time Blocking Optimization
  if (analysis.hasGaps && analysis.gaps.length > 0) {
    suggestions.push(generateTimeBlockingSuggestion(analysis))
  }
  
  // 2. Break Recommendations
  if (analysis.workBlocks.length > 0 && analysis.breakBlocks.length < 2) {
    suggestions.push(generateBreakSuggestion(analysis))
  }
  
  // 3. Energy Management
  if (analysis.needsEnergyOptimization) {
    suggestions.push(generateEnergySuggestion(analysis))
  }
  
  // 4. Productivity Balance
  if (analysis.productivityScore < 70) {
    suggestions.push(generateProductivitySuggestion(analysis))
  }
  
  // 5. Daily Planning
  if (existingBlocks.length === 0) {
    suggestions.push(generateDailyPlanningSuggestion())
  }
  
  return suggestions
}

// Fallback chat response for when backend is not available
const getFallbackChatResponse = async (message, conversationId) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  const responses = [
    "I can help you with scheduling and productivity tips! While the full AI backend isn't connected, I can still provide helpful suggestions based on proven productivity principles.",
    "Great question! For optimal scheduling, I recommend time-blocking your most important tasks during your peak energy hours (usually 9-11 AM). Would you like me to suggest some time blocks for your day?",
    "I'd be happy to help with your schedule! Try breaking your day into focused work blocks of 2-3 hours with 15-30 minute breaks in between. This helps maintain energy and focus throughout the day.",
    "Excellent question! For better productivity, consider scheduling your most challenging tasks during your natural energy peaks and save meetings for your lower-energy periods.",
    "I can definitely help with that! A well-structured day typically includes: morning deep work (9-11 AM), collaborative work (2-4 PM), and personal time in the evening. Would you like me to create a sample schedule for you?"
  ]
  
  const randomResponse = responses[Math.floor(Math.random() * responses.length)]
  
  return {
    response: randomResponse,
    conversationId: conversationId || `fallback-${Date.now()}`,
    sources: [],
    agentActions: [],
    confidence: 0.7
  }
}

// New RAG-powered chat function
export const chatWithAI = async (message, conversationId = null, useRAG = true, useAgents = false) => {
  // Skip API call in production if no backend is configured
  if (isProduction && !process.env.REACT_APP_API_URL) {
    return getFallbackChatResponse(message, conversationId)
  }

  try {
    const response = await fetch(`${API_BASE_URL}/chat/message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        use_rag: useRAG,
        use_agents: useAgents,
        context: {
          app: 'ai-scheduler',
          timestamp: new Date().toISOString()
        }
      })
    })

    if (response.ok) {
      const data = await response.json()
      return {
        response: data.response,
        conversationId: data.conversation_id,
        sources: data.sources || [],
        agentActions: data.agent_actions || [],
        confidence: data.confidence || 0
      }
    } else {
      throw new Error(`API request failed: ${response.status}`)
    }
  } catch (error) {
    console.error('Error chatting with AI:', error)
    return getFallbackChatResponse(message, conversationId)
  }
}

// Document upload function
export const uploadDocument = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
      method: 'POST',
      body: formData
    })

    if (response.ok) {
      const data = await response.json()
      return {
        success: true,
        documentId: data.document_id,
        filename: data.filename,
        chunksProcessed: data.chunks_processed
      }
    } else {
      throw new Error(`Upload failed: ${response.status}`)
    }
  } catch (error) {
    console.error('Error uploading document:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

// Agent task execution
export const executeAgentTask = async (task, agentType = 'general') => {
  try {
    const response = await fetch(`${API_BASE_URL}/agents/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        task,
        agent_type: agentType,
        parameters: {}
      })
    })

    if (response.ok) {
      const data = await response.json()
      return {
        success: true,
        taskId: data.task_id,
        status: data.status,
        result: data.result
      }
    } else {
      throw new Error(`Agent execution failed: ${response.status}`)
    }
  } catch (error) {
    console.error('Error executing agent task:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

// Search knowledge base
export const searchKnowledgeBase = async (query, limit = 10) => {
  try {
    const response = await fetch(`${API_BASE_URL}/search?query=${encodeURIComponent(query)}&limit=${limit}`)

    if (response.ok) {
      const data = await response.json()
      return {
        success: true,
        results: data.results,
        totalFound: data.total_found
      }
    } else {
      throw new Error(`Search failed: ${response.status}`)
    }
  } catch (error) {
    console.error('Error searching knowledge base:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

// Analyze current schedule for patterns and opportunities
const analyzeSchedule = (blocks) => {
  const workBlocks = blocks.filter(b => b.category === 'work')
  const breakBlocks = blocks.filter(b => b.category === 'break')
  const meetingBlocks = blocks.filter(b => b.category === 'meeting')
  
  const gaps = findScheduleGaps(blocks)
  const totalWorkTime = workBlocks.reduce((sum, b) => sum + (b.endTime - b.startTime), 0)
  const hasLongWorkBlocks = workBlocks.some(b => (b.endTime - b.startTime) > 4)
  const needsEnergyOptimization = totalWorkTime > 8 || hasLongWorkBlocks
  
  const productivityScore = calculateProductivityScore(blocks)
  
  return {
    workBlocks,
    breakBlocks,
    meetingBlocks,
    gaps,
    totalWorkTime,
    hasGaps: gaps.length > 0,
    needsEnergyOptimization,
    productivityScore,
    hasLongWorkBlocks
  }
}

// Find gaps in the schedule
const findScheduleGaps = (blocks) => {
  const gaps = []
  const sortedBlocks = [...blocks].sort((a, b) => a.startTime - b.startTime)
  
  for (let i = 0; i < sortedBlocks.length - 1; i++) {
    const currentEnd = sortedBlocks[i].endTime
    const nextStart = sortedBlocks[i + 1].startTime
    
    if (nextStart - currentEnd >= 1) { // Gap of at least 1 hour
      gaps.push({
        start: currentEnd,
        end: nextStart,
        duration: nextStart - currentEnd
      })
    }
  }
  
  return gaps
}

// Calculate productivity score
const calculateProductivityScore = (blocks) => {
  if (blocks.length === 0) return 0
  
  let score = 0
  const totalTime = blocks.reduce((sum, b) => sum + (b.endTime - b.startTime), 0)
  
  blocks.forEach(block => {
    const duration = block.endTime - block.startTime
    
    // Base score
    score += duration * 10
    
    // Category bonuses
    const bonuses = {
      work: 5,
      learning: 7,
      exercise: 8,
      break: 3,
      meeting: 4,
      personal: 2
    }
    
    score += duration * (bonuses[block.category] || 3)
    
    // Optimal time bonuses
    if (block.category === 'work' && block.startTime >= 9 && block.startTime <= 11) {
      score += duration * 3
    }
    
    // Penalty for very long blocks
    if (duration > 4) {
      score -= (duration - 4) * 5
    }
  })
  
  return Math.min(100, Math.round(score / totalTime * 10))
}

// Generate time blocking optimization suggestion
const generateTimeBlockingSuggestion = (analysis) => {
  const largestGap = analysis.gaps.reduce((max, gap) => 
    gap.duration > max.duration ? gap : max, analysis.gaps[0])
  
  const suggestions = []
  
  if (largestGap.duration >= 2) {
    suggestions.push({
      title: 'Deep Work Block',
      category: 'work',
      startTime: largestGap.start,
      endTime: largestGap.start + 2,
      description: 'Use this time for focused, uninterrupted work'
    })
  }
  
  if (largestGap.duration >= 3) {
    suggestions.push({
      title: 'Learning Time',
      category: 'learning',
      startTime: largestGap.start + 2,
      endTime: largestGap.start + 3,
      description: 'Dedicated time for skill development'
    })
  }
  
  return {
    type: 'optimization',
    title: 'Optimize Your Schedule',
    description: `You have a ${Math.round(largestGap.duration)}-hour gap in your schedule that could be used more productively.`,
    blocks: suggestions,
    reasons: [
      'Leverages your natural energy patterns',
      'Creates dedicated focus time',
      'Improves overall productivity',
      'Reduces context switching'
    ]
  }
}

// Generate break recommendation
const generateBreakSuggestion = (analysis) => {
  const workBlocks = analysis.workBlocks
  const breakTime = workBlocks.length > 0 ? workBlocks[0].endTime + 0.5 : 12
  
  return {
    type: 'timeblocking',
    title: 'Add Strategic Breaks',
    description: 'Taking regular breaks improves focus and prevents burnout. Consider adding break time between work blocks.',
    blocks: [
      {
        title: 'Coffee Break',
        category: 'break',
        startTime: breakTime,
        endTime: breakTime + 0.5,
        description: 'Short break to recharge and refocus'
      }
    ],
    reasons: [
      'Improves focus and concentration',
      'Prevents decision fatigue',
      'Boosts creativity and problem-solving',
      'Maintains consistent energy levels'
    ]
  }
}

// Generate energy management suggestion
const generateEnergySuggestion = (analysis) => {
  const suggestions = []
  
  if (analysis.totalWorkTime > 8) {
    suggestions.push({
      title: 'Energy Recharge',
      category: 'break',
      startTime: 14,
      endTime: 15,
      description: 'Extended break to maintain energy throughout the day'
    })
  }
  
  if (analysis.hasLongWorkBlocks) {
    suggestions.push({
      title: 'Micro Break',
      category: 'break',
      startTime: 11,
      endTime: 11.25,
      description: 'Short break to maintain focus during long work sessions'
    })
  }
  
  return {
    type: 'balance',
    title: 'Optimize Your Energy',
    description: 'Your schedule could benefit from better energy management to maintain peak performance.',
    blocks: suggestions,
    reasons: [
      'Prevents afternoon energy crashes',
      'Maintains consistent performance',
      'Reduces stress and burnout',
      'Improves decision-making quality'
    ]
  }
}

// Generate productivity improvement suggestion
const generateProductivitySuggestion = (analysis) => {
  const suggestions = [
    {
      title: 'Morning Deep Work',
      category: 'work',
      startTime: 9,
      endTime: 11,
      description: 'Peak focus hours for your most important tasks'
    },
    {
      title: 'Exercise Break',
      category: 'exercise',
      startTime: 18,
      endTime: 19,
      description: 'Physical activity to boost energy and mental clarity'
    }
  ]
  
  return {
    type: 'productivity',
    title: 'Boost Your Productivity',
    description: `Your current productivity score is ${analysis.productivityScore}/100. Here are some suggestions to improve it.`,
    blocks: suggestions,
    reasons: [
      'Aligns with natural energy rhythms',
      'Creates work-life balance',
      'Improves focus and concentration',
      'Builds sustainable habits'
    ]
  }
}

// Generate daily planning suggestion for empty schedule
const generateDailyPlanningSuggestion = () => {
  return {
    type: 'timeblocking',
    title: 'Plan Your Perfect Day',
    description: 'Start with a well-structured daily schedule that balances work, breaks, and personal time.',
    blocks: [
      {
        title: 'Morning Deep Work',
        category: 'work',
        startTime: 9,
        endTime: 11,
        description: 'Focus on your most important tasks when energy is highest'
      },
      {
        title: 'Lunch Break',
        category: 'break',
        startTime: 12,
        endTime: 13,
        description: 'Nourish your body and mind with a proper lunch break'
      },
      {
        title: 'Afternoon Tasks',
        category: 'work',
        startTime: 14,
        endTime: 16,
        description: 'Handle meetings and collaborative work'
      },
      {
        title: 'Personal Time',
        category: 'personal',
        startTime: 19,
        endTime: 20,
        description: 'Time for hobbies, family, or relaxation'
      }
    ],
    reasons: [
      'Follows proven productivity patterns',
      'Balances focused work with breaks',
      'Respects natural energy cycles',
      'Creates sustainable daily rhythm'
    ]
  }
}
