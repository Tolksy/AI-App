import React, { useState } from 'react'
import { format, isSameMonth, isSameDay, startOfMonth, endOfMonth, eachDayOfInterval, isWithinInterval, addMonths, subMonths } from 'date-fns'
import { ChevronLeft, ChevronRight } from 'lucide-react'

const Calendar = ({ selectedDate, onDateSelect, timeBlocks }) => {
  const [currentMonth, setCurrentMonth] = useState(selectedDate)

  const monthStart = startOfMonth(currentMonth)
  const monthEnd = endOfMonth(currentMonth)
  const calendarDays = eachDayOfInterval({ start: monthStart, end: monthEnd })

  // Get days from previous month to fill the grid
  const startDate = monthStart
  const prevMonthDays = []
  const startDayOfWeek = startDate.getDay()
  
  for (let i = startDayOfWeek - 1; i >= 0; i--) {
    const prevDay = new Date(startDate)
    prevDay.setDate(prevDay.getDate() - (i + 1))
    prevMonthDays.push(prevDay)
  }

  // Get days from next month to fill the grid
  const endDate = monthEnd
  const nextMonthDays = []
  const endDayOfWeek = endDate.getDay()
  
  for (let i = 1; i <= (6 - endDayOfWeek); i++) {
    const nextDay = new Date(endDate)
    nextDay.setDate(nextDay.getDate() + i)
    nextMonthDays.push(nextDay)
  }

  const allDays = [...prevMonthDays, ...calendarDays, ...nextMonthDays]

  const hasBlocksOnDate = (date) => {
    const dateKey = date.toDateString()
    return timeBlocks[dateKey] && timeBlocks[dateKey].length > 0
  }

  const getBlockCount = (date) => {
    const dateKey = date.toDateString()
    return timeBlocks[dateKey] ? timeBlocks[dateKey].length : 0
  }

  const navigateMonth = (direction) => {
    if (direction === 'prev') {
      setCurrentMonth(subMonths(currentMonth, 1))
    } else {
      setCurrentMonth(addMonths(currentMonth, 1))
    }
  }

  const isCurrentMonth = (date) => {
    return isSameMonth(date, currentMonth)
  }

  const isSelected = (date) => {
    return isSameDay(date, selectedDate)
  }

  const isToday = (date) => {
    return isSameDay(date, new Date())
  }

  return (
    <div className="calendar">
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: '16px' 
      }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1a202c' }}>
          {format(currentMonth, 'MMMM yyyy')}
        </h3>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button 
            onClick={() => navigateMonth('prev')}
            className="btn btn-secondary"
            style={{ padding: '8px' }}
          >
            <ChevronLeft size={16} />
          </button>
          <button 
            onClick={() => navigateMonth('next')}
            className="btn btn-secondary"
            style={{ padding: '8px' }}
          >
            <ChevronRight size={16} />
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: '4px' }}>
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div 
            key={day} 
            style={{ 
              padding: '8px', 
              textAlign: 'center', 
              fontSize: '12px', 
              fontWeight: '600', 
              color: '#64748b',
              backgroundColor: '#f8fafc'
            }}
          >
            {day}
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: '4px' }}>
        {allDays.map((day, index) => (
          <button
            key={index}
            onClick={() => onDateSelect(day)}
            style={{
              padding: '12px 8px',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500',
              backgroundColor: isSelected(day) 
                ? '#667eea' 
                : isToday(day) 
                  ? '#f0f4ff' 
                  : 'transparent',
              color: isSelected(day) 
                ? 'white' 
                : !isCurrentMonth(day) 
                  ? '#cbd5e1' 
                  : isToday(day) 
                    ? '#667eea' 
                    : '#374151',
              position: 'relative',
              transition: 'all 0.2s ease',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              minHeight: '48px'
            }}
            onMouseEnter={(e) => {
              if (!isSelected(day)) {
                e.target.style.backgroundColor = '#f1f5f9'
              }
            }}
            onMouseLeave={(e) => {
              if (!isSelected(day)) {
                e.target.style.backgroundColor = isToday(day) ? '#f0f4ff' : 'transparent'
              }
            }}
          >
            <span>{format(day, 'd')}</span>
            {hasBlocksOnDate(day) && (
              <div style={{
                position: 'absolute',
                bottom: '4px',
                left: '50%',
                transform: 'translateX(-50%)',
                width: '6px',
                height: '6px',
                borderRadius: '50%',
                backgroundColor: isSelected(day) ? 'white' : '#667eea'
              }} />
            )}
            {getBlockCount(day) > 1 && (
              <span style={{
                position: 'absolute',
                top: '2px',
                right: '2px',
                fontSize: '10px',
                fontWeight: '600',
                backgroundColor: '#667eea',
                color: 'white',
                borderRadius: '50%',
                width: '16px',
                height: '16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {getBlockCount(day)}
              </span>
            )}
          </button>
        ))}
      </div>
    </div>
  )
}

export default Calendar
