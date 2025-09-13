import React from 'react'
import { format } from 'date-fns'
import { Edit, Trash2, Plus } from 'lucide-react'

const TimeBlock = ({ 
  selectedDate, 
  timeSlots, 
  timeBlocks, 
  onTimeSlotClick, 
  onEditBlock, 
  onDeleteBlock 
}) => {
  const dateKey = selectedDate.toDateString()
  const dayBlocks = timeBlocks[dateKey] || []

  const getBlocksForTimeSlot = (timeSlot) => {
    return dayBlocks.filter(block => {
      const blockStart = parseInt(block.startTime)
      const blockEnd = parseInt(block.endTime)
      return timeSlot >= blockStart && timeSlot < blockEnd
    })
  }

  const getBlockHeight = (block) => {
    const duration = parseInt(block.endTime) - parseInt(block.startTime)
    return duration * 40 // 40px per hour
  }

  const getBlockPosition = (block) => {
    const startHour = parseInt(block.startTime)
    const startMinute = (block.startTime - startHour) * 60
    return (startHour - 6) * 40 + (startMinute / 60) * 40 // 6 AM is the start time
  }

  const formatTime = (hour) => {
    const period = hour >= 12 ? 'PM' : 'AM'
    const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour
    return `${displayHour}:00 ${period}`
  }

  const getCategoryColor = (category) => {
    const colors = {
      work: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      break: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      meeting: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      personal: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
      exercise: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
      learning: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
    }
    return colors[category] || colors.work
  }

  return (
    <div className="time-block-container">
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: '16px' 
      }}>
        <h3 style={{ fontSize: '16px', fontWeight: '600', color: '#1a202c' }}>
          {format(selectedDate, 'EEEE, MMMM d')}
        </h3>
        <button 
          className="btn btn-primary"
          onClick={() => onTimeSlotClick(9)} // Default to 9 AM
          style={{ padding: '8px 16px', fontSize: '12px' }}
        >
          <Plus size={14} />
          Add Block
        </button>
      </div>

      <div style={{ position: 'relative' }}>
        <div className="time-grid">
          {timeSlots.map(timeSlot => {
            const blocks = getBlocksForTimeSlot(timeSlot)
            
            return (
              <div key={timeSlot} style={{ display: 'contents' }}>
                <div className="time-slot">
                  {formatTime(timeSlot)}
                </div>
                <div 
                  className="time-content"
                  onClick={() => onTimeSlotClick(timeSlot)}
                  style={{ 
                    cursor: 'pointer',
                    minHeight: '40px',
                    position: 'relative',
                    display: 'flex',
                    alignItems: 'center',
                    padding: '4px'
                  }}
                >
                  {blocks.length === 0 && (
                    <div style={{
                      width: '100%',
                      height: '100%',
                      border: '2px dashed #e2e8f0',
                      borderRadius: '4px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#94a3b8',
                      fontSize: '12px',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.target.style.borderColor = '#667eea'
                      e.target.style.color = '#667eea'
                      e.target.style.backgroundColor = '#f0f4ff'
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.borderColor = '#e2e8f0'
                      e.target.style.color = '#94a3b8'
                      e.target.style.backgroundColor = 'transparent'
                    }}
                    >
                      Click to add block
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Render time blocks */}
        <div style={{ 
          position: 'absolute', 
          top: 0, 
          left: '60px', 
          right: 0,
          pointerEvents: 'none'
        }}>
          {dayBlocks.map(block => (
            <div
              key={block.id}
              style={{
                position: 'absolute',
                top: `${getBlockPosition(block)}px`,
                left: '4px',
                right: '4px',
                height: `${getBlockHeight(block)}px`,
                background: getCategoryColor(block.category),
                borderRadius: '6px',
                padding: '8px',
                color: 'white',
                fontSize: '12px',
                fontWeight: '500',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                cursor: 'pointer',
                pointerEvents: 'auto',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                transition: 'transform 0.2s ease',
                zIndex: 1
              }}
              onMouseEnter={(e) => {
                e.target.style.transform = 'scale(1.02)'
                e.target.style.zIndex = 10
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'scale(1)'
                e.target.style.zIndex = 1
              }}
              onClick={() => onEditBlock(block)}
            >
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ 
                  fontWeight: '600', 
                  marginBottom: '2px',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap'
                }}>
                  {block.title}
                </div>
                <div style={{ 
                  fontSize: '10px', 
                  opacity: 0.9,
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap'
                }}>
                  {formatTime(block.startTime)} - {formatTime(block.endTime)}
                </div>
              </div>
              <div style={{ 
                display: 'flex', 
                gap: '4px', 
                opacity: 0,
                transition: 'opacity 0.2s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.opacity = '1'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.opacity = '0'
              }}
              >
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    onEditBlock(block)
                  }}
                  style={{
                    background: 'rgba(255,255,255,0.2)',
                    border: 'none',
                    borderRadius: '4px',
                    padding: '4px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  <Edit size={12} />
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    onDeleteBlock(block.id)
                  }}
                  style={{
                    background: 'rgba(255,255,255,0.2)',
                    border: 'none',
                    borderRadius: '4px',
                    padding: '4px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  <Trash2 size={12} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {dayBlocks.length === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '40px 20px',
          color: '#64748b',
          fontSize: '14px'
        }}>
          <div style={{ marginBottom: '8px', fontSize: '48px' }}>📅</div>
          <div style={{ fontWeight: '500', marginBottom: '4px' }}>No blocks scheduled</div>
          <div>Click on a time slot to add your first time block</div>
        </div>
      )}
    </div>
  )
}

export default TimeBlock
