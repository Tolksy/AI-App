import React, { useState, useEffect } from 'react'
import { X } from 'lucide-react'

const ScheduleModal = ({ isOpen, onClose, onSave, initialData, selectedDate }) => {
  const [formData, setFormData] = useState({
    title: '',
    category: 'work',
    startTime: 9,
    endTime: 10,
    description: ''
  })

  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title || '',
        category: initialData.category || 'work',
        startTime: initialData.startTime || 9,
        endTime: initialData.endTime || 10,
        description: initialData.description || ''
      })
    } else {
      setFormData({
        title: '',
        category: 'work',
        startTime: 9,
        endTime: 10,
        description: ''
      })
    }
  }, [initialData])

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!formData.title.trim()) {
      alert('Please enter a title for the time block')
      return
    }

    if (formData.startTime >= formData.endTime) {
      alert('End time must be after start time')
      return
    }

    const blockData = {
      ...formData,
      date: selectedDate,
      startTime: formData.startTime,
      endTime: formData.endTime
    }

    onSave(blockData)
  }

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const categories = [
    { value: 'work', label: 'Work', emoji: '💼' },
    { value: 'meeting', label: 'Meeting', emoji: '🤝' },
    { value: 'break', label: 'Break', emoji: '☕' },
    { value: 'personal', label: 'Personal', emoji: '👤' },
    { value: 'exercise', label: 'Exercise', emoji: '🏃' },
    { value: 'learning', label: 'Learning', emoji: '📚' }
  ]

  const generateTimeOptions = () => {
    const options = []
    for (let hour = 6; hour <= 22; hour++) {
      for (let minute = 0; minute < 60; minute += 30) {
        const timeValue = hour + (minute / 60)
        const period = hour >= 12 ? 'PM' : 'AM'
        const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour
        const displayMinute = minute === 0 ? '00' : minute.toString()
        const timeString = `${displayHour}:${displayMinute} ${period}`
        options.push({ value: timeValue, label: timeString })
      }
    }
    return options
  }

  const timeOptions = generateTimeOptions()

  if (!isOpen) return null

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">
            {initialData ? 'Edit Time Block' : 'Add Time Block'}
          </h2>
          <button className="close-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Title *</label>
            <input
              type="text"
              className="input"
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              placeholder="Enter block title..."
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Category</label>
            <select
              className="form-select"
              value={formData.category}
              onChange={(e) => handleInputChange('category', e.target.value)}
            >
              {categories.map(category => (
                <option key={category.value} value={category.value}>
                  {category.emoji} {category.label}
                </option>
              ))}
            </select>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">Start Time</label>
              <select
                className="form-select"
                value={formData.startTime}
                onChange={(e) => handleInputChange('startTime', parseFloat(e.target.value))}
              >
                {timeOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">End Time</label>
              <select
                className="form-select"
                value={formData.endTime}
                onChange={(e) => handleInputChange('endTime', parseFloat(e.target.value))}
              >
                {timeOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Description</label>
            <textarea
              className="input"
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              placeholder="Add notes or details..."
              rows={3}
              style={{ resize: 'vertical' }}
            />
          </div>

          <div style={{ 
            display: 'flex', 
            justifyContent: 'flex-end', 
            gap: '12px',
            marginTop: '24px'
          }}>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
            >
              {initialData ? 'Update Block' : 'Add Block'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ScheduleModal
