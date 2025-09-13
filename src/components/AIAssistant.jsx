import React, { useState } from 'react'
import { Brain, Lightbulb, Clock, TrendingUp, CheckCircle, Sparkles } from 'lucide-react'

const AIAssistant = ({ selectedDate, suggestions, onApplySuggestion, isLoading }) => {
  const [expandedSuggestion, setExpandedSuggestion] = useState(null)

  const getSuggestionIcon = (type) => {
    const icons = {
      optimization: <TrendingUp size={16} />,
      timeblocking: <Clock size={16} />,
      productivity: <Lightbulb size={16} />,
      balance: <CheckCircle size={16} />
    }
    return icons[type] || <Sparkles size={16} />
  }

  const getSuggestionColor = (type) => {
    const colors = {
      optimization: '#667eea',
      timeblocking: '#4facfe',
      productivity: '#43e97b',
      balance: '#f093fb'
    }
    return colors[type] || '#667eea'
  }

  const formatTime = (hour) => {
    const period = hour >= 12 ? 'PM' : 'AM'
    const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour
    return `${displayHour}:00 ${period}`
  }

  const getCategoryEmoji = (category) => {
    const emojis = {
      work: '💼',
      meeting: '🤝',
      break: '☕',
      personal: '👤',
      exercise: '🏃',
      learning: '📚'
    }
    return emojis[category] || '📝'
  }

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <span style={{ marginLeft: '12px', color: '#64748b' }}>
          AI is analyzing your schedule...
        </span>
      </div>
    )
  }

  if (suggestions.length === 0) {
    return (
      <div style={{
        textAlign: 'center',
        padding: '40px 20px',
        color: '#64748b'
      }}>
        <Brain size={48} color="#cbd5e1" style={{ marginBottom: '16px' }} />
        <div style={{ fontSize: '16px', fontWeight: '500', marginBottom: '8px' }}>
          No AI suggestions yet
        </div>
        <div style={{ fontSize: '14px' }}>
          Add some time blocks to get personalized scheduling recommendations
        </div>
      </div>
    )
  }

  return (
    <div className="ai-assistant">
      <div style={{ marginBottom: '16px', fontSize: '14px', color: '#64748b' }}>
        Based on your current schedule and best practices, here are some AI-powered suggestions:
      </div>

      {suggestions.map((suggestion, index) => (
        <div key={index} className="ai-suggestion">
          <div 
            className="suggestion-title"
            style={{ cursor: 'pointer' }}
            onClick={() => setExpandedSuggestion(expandedSuggestion === index ? null : index)}
          >
            <div style={{ 
              color: getSuggestionColor(suggestion.type),
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              {getSuggestionIcon(suggestion.type)}
              {suggestion.title}
            </div>
            <div style={{ 
              fontSize: '12px', 
              color: '#64748b',
              marginLeft: 'auto'
            }}>
              {expandedSuggestion === index ? 'Hide details' : 'Show details'}
            </div>
          </div>

          <div className="suggestion-text">
            {suggestion.description}
          </div>

          {expandedSuggestion === index && (
            <div style={{ marginTop: '16px' }}>
              {suggestion.blocks && suggestion.blocks.length > 0 && (
                <div>
                  <div style={{ 
                    fontSize: '14px', 
                    fontWeight: '600', 
                    marginBottom: '12px',
                    color: '#374151'
                  }}>
                    Suggested Time Blocks:
                  </div>
                  <div style={{ display: 'grid', gap: '8px' }}>
                    {suggestion.blocks.map((block, blockIndex) => (
                      <div key={blockIndex} style={{
                        background: 'rgba(255,255,255,0.7)',
                        borderRadius: '8px',
                        padding: '12px',
                        border: '1px solid rgba(0,0,0,0.1)'
                      }}>
                        <div style={{ 
                          display: 'flex', 
                          alignItems: 'center', 
                          gap: '8px',
                          marginBottom: '4px'
                        }}>
                          <span style={{ fontSize: '16px' }}>
                            {getCategoryEmoji(block.category)}
                          </span>
                          <span style={{ fontWeight: '600', fontSize: '14px' }}>
                            {block.title}
                          </span>
                          <span style={{ 
                            fontSize: '12px', 
                            color: '#64748b',
                            marginLeft: 'auto'
                          }}>
                            {formatTime(block.startTime)} - {formatTime(block.endTime)}
                          </span>
                        </div>
                        {block.description && (
                          <div style={{ 
                            fontSize: '12px', 
                            color: '#64748b',
                            fontStyle: 'italic'
                          }}>
                            {block.description}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {suggestion.reasons && (
                <div style={{ marginTop: '16px' }}>
                  <div style={{ 
                    fontSize: '14px', 
                    fontWeight: '600', 
                    marginBottom: '8px',
                    color: '#374151'
                  }}>
                    Why this helps:
                  </div>
                  <ul style={{ 
                    paddingLeft: '20px',
                    fontSize: '13px',
                    color: '#64748b',
                    lineHeight: '1.5'
                  }}>
                    {suggestion.reasons.map((reason, reasonIndex) => (
                      <li key={reasonIndex} style={{ marginBottom: '4px' }}>
                        {reason}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div style={{ 
                display: 'flex', 
                justifyContent: 'flex-end',
                marginTop: '16px',
                gap: '8px'
              }}>
                <button
                  className="btn btn-secondary"
                  onClick={() => setExpandedSuggestion(null)}
                  style={{ padding: '8px 16px', fontSize: '12px' }}
                >
                  Dismiss
                </button>
                <button
                  className="btn btn-primary"
                  onClick={() => onApplySuggestion(suggestion)}
                  style={{ padding: '8px 16px', fontSize: '12px' }}
                >
                  Apply Suggestion
                </button>
              </div>
            </div>
          )}
        </div>
      ))}

      <div style={{
        marginTop: '20px',
        padding: '12px',
        background: 'rgba(102, 126, 234, 0.1)',
        borderRadius: '8px',
        fontSize: '12px',
        color: '#667eea',
        textAlign: 'center'
      }}>
        💡 AI suggestions are based on productivity research and time management best practices
      </div>
    </div>
  )
}

export default AIAssistant
