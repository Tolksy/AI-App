// AI Service for generating intelligent scheduling suggestions
// This is a mock AI service that simulates AI recommendations based on productivity research

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

// Generate AI suggestions based on current schedule
export const getAISuggestions = async (selectedDate, existingBlocks) => {
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
