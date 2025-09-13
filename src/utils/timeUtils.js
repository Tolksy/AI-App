import { format, isToday, isTomorrow, isYesterday, addDays, startOfDay, endOfDay } from 'date-fns'

// Generate time slots from 6 AM to 10 PM in 30-minute intervals
export const generateTimeSlots = () => {
  const slots = []
  for (let hour = 6; hour <= 22; hour++) {
    for (let minute = 0; minute < 60; minute += 30) {
      slots.push(hour + (minute / 60))
    }
  }
  return slots
}

// Format time from decimal hours to readable format
export const formatTime = (hour) => {
  const period = hour >= 12 ? 'PM' : 'AM'
  const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour
  const minutes = Math.round((hour % 1) * 60)
  const displayMinute = minutes === 0 ? '00' : minutes.toString().padStart(2, '0')
  return `${displayHour}:${displayMinute} ${period}`
}

// Format date for display
export const formatDate = (date) => {
  if (isToday(date)) return 'Today'
  if (isTomorrow(date)) return 'Tomorrow'
  if (isYesterday(date)) return 'Yesterday'
  
  return format(date, 'EEEE, MMMM d, yyyy')
}

// Get relative date description
export const getRelativeDate = (date) => {
  const today = startOfDay(new Date())
  const targetDate = startOfDay(date)
  const diffInDays = Math.ceil((targetDate - today) / (1000 * 60 * 60 * 24))
  
  if (diffInDays === 0) return 'Today'
  if (diffInDays === 1) return 'Tomorrow'
  if (diffInDays === -1) return 'Yesterday'
  if (diffInDays > 1) return `In ${diffInDays} days`
  if (diffInDays < -1) return `${Math.abs(diffInDays)} days ago`
  
  return format(date, 'MMMM d, yyyy')
}

// Calculate duration between two times
export const calculateDuration = (startTime, endTime) => {
  return endTime - startTime
}

// Format duration in hours and minutes
export const formatDuration = (duration) => {
  const hours = Math.floor(duration)
  const minutes = Math.round((duration % 1) * 60)
  
  if (hours === 0) return `${minutes}m`
  if (minutes === 0) return `${hours}h`
  return `${hours}h ${minutes}m`
}

// Check if two time blocks overlap
export const blocksOverlap = (block1, block2) => {
  const start1 = block1.startTime
  const end1 = block1.endTime
  const start2 = block2.startTime
  const end2 = block2.endTime
  
  return start1 < end2 && start2 < end1
}

// Find overlapping blocks
export const findOverlappingBlocks = (blocks) => {
  const overlaps = []
  
  for (let i = 0; i < blocks.length; i++) {
    for (let j = i + 1; j < blocks.length; j++) {
      if (blocksOverlap(blocks[i], blocks[j])) {
        overlaps.push([blocks[i], blocks[j]])
      }
    }
  }
  
  return overlaps
}

// Get available time slots for a given day
export const getAvailableSlots = (blocks, dayStart = 6, dayEnd = 22) => {
  const occupiedSlots = []
  
  blocks.forEach(block => {
    const start = Math.max(block.startTime, dayStart)
    const end = Math.min(block.endTime, dayEnd)
    
    for (let hour = Math.floor(start); hour < Math.ceil(end); hour++) {
      for (let minute = 0; minute < 60; minute += 30) {
        const slot = hour + (minute / 60)
        if (slot >= start && slot < end) {
          occupiedSlots.push(slot)
        }
      }
    }
  })
  
  const allSlots = generateTimeSlots().filter(slot => slot >= dayStart && slot <= dayEnd)
  return allSlots.filter(slot => !occupiedSlots.includes(slot))
}

// Get the next available time slot
export const getNextAvailableSlot = (blocks, preferredTime = 9) => {
  const availableSlots = getAvailableSlots(blocks)
  return availableSlots.find(slot => slot >= preferredTime) || availableSlots[0]
}

// Validate time block
export const validateTimeBlock = (block) => {
  const errors = []
  
  if (!block.title || block.title.trim().length === 0) {
    errors.push('Title is required')
  }
  
  if (block.startTime >= block.endTime) {
    errors.push('End time must be after start time')
  }
  
  if (block.startTime < 6 || block.startTime > 22) {
    errors.push('Start time must be between 6 AM and 10 PM')
  }
  
  if (block.endTime < 6 || block.endTime > 22) {
    errors.push('End time must be between 6 AM and 10 PM')
  }
  
  return errors
}

// Get productivity score based on schedule
export const getProductivityScore = (blocks) => {
  if (blocks.length === 0) return 0
  
  let score = 0
  let totalTime = 0
  
  blocks.forEach(block => {
    const duration = calculateDuration(block.startTime, block.endTime)
    totalTime += duration
    
    // Base score for having scheduled time
    score += duration * 10
    
    // Bonus for work blocks
    if (block.category === 'work') {
      score += duration * 5
    }
    
    // Bonus for breaks
    if (block.category === 'break') {
      score += duration * 3
    }
    
    // Bonus for exercise
    if (block.category === 'exercise') {
      score += duration * 8
    }
    
    // Bonus for learning
    if (block.category === 'learning') {
      score += duration * 7
    }
  })
  
  // Penalty for very long blocks (>4 hours)
  blocks.forEach(block => {
    const duration = calculateDuration(block.startTime, block.endTime)
    if (duration > 4) {
      score -= (duration - 4) * 5
    }
  })
  
  // Normalize to 0-100 scale
  return Math.min(100, Math.max(0, Math.round(score / Math.max(totalTime, 1) * 10)))
}
