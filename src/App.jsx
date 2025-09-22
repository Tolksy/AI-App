import React, { useState, useEffect } from 'react'

function App() {
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState('')
  const [leads, setLeads] = useState([])
  const [loading, setLoading] = useState(false)

  // Test backend connection on load
  useEffect(() => {
    fetchLeads()
  }, [])

  const fetchLeads = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/leads/')
      const data = await res.json()
      setLeads(data)
    } catch (error) {
      console.error('Error fetching leads:', error)
    }
  }

  const sendMessage = async () => {
    if (!message.trim()) return
    
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/v1/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          conversation_id: 'test-conversation'
        })
      })
      const data = await res.json()
      setResponse(data.response)
      setMessage('')
    } catch (error) {
      console.error('Error sending message:', error)
      setResponse('Error: Could not connect to backend')
    }
    setLoading(false)
  }

  return (
    <div style={{ 
      padding: '20px', 
      maxWidth: '1200px', 
      margin: '0 auto',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1 style={{ color: '#2c3e50', textAlign: 'center' }}>
        AI Lead Generation Agent - MVP
      </h1>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: '1fr 1fr', 
        gap: '20px',
        marginTop: '20px'
      }}>
        {/* Chat Section */}
        <div style={{ 
          border: '1px solid #ddd', 
          borderRadius: '8px', 
          padding: '20px',
          backgroundColor: '#f9f9f9'
        }}>
          <h2>Chat with AI Agent</h2>
          <div style={{ marginBottom: '10px' }}>
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask about lead generation..."
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                marginBottom: '10px'
              }}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              style={{
                padding: '10px 20px',
                backgroundColor: '#3498db',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              {loading ? 'Sending...' : 'Send'}
            </button>
          </div>
          {response && (
            <div style={{
              backgroundColor: '#e8f4fd',
              padding: '10px',
              borderRadius: '4px',
              border: '1px solid #3498db'
            }}>
              <strong>AI Response:</strong> {response}
            </div>
          )}
        </div>

        {/* Leads Section */}
        <div style={{ 
          border: '1px solid #ddd', 
          borderRadius: '8px', 
          padding: '20px',
          backgroundColor: '#f9f9f9'
        }}>
          <h2>Generated Leads ({leads.length})</h2>
          {leads.length > 0 ? (
            <div>
              {leads.map(lead => (
                <div key={lead.id} style={{
                  border: '1px solid #eee',
                  borderRadius: '4px',
                  padding: '10px',
                  marginBottom: '10px',
                  backgroundColor: 'white'
                }}>
                  <strong>{lead.name}</strong> - {lead.company}<br/>
                  <small>{lead.email} | {lead.industry} | {lead.status}</small>
                </div>
              ))}
            </div>
          ) : (
            <p>No leads found. Try chatting with the AI to generate some!</p>
          )}
        </div>
      </div>

      <div style={{ 
        marginTop: '20px', 
        textAlign: 'center',
        color: '#7f8c8d'
      }}>
        <p>Backend: http://localhost:8000 | Frontend: http://localhost:3000</p>
        <p>Status: {leads.length > 0 ? '✅ Connected' : '❌ Not connected'}</p>
      </div>
    </div>
  )
}

export default App
