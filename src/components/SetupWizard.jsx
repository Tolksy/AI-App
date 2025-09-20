import React, { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

export default function SetupWizard() {
  const [verifyTokenSet, setVerifyTokenSet] = useState(false)
  const [pageTokenSet, setPageTokenSet] = useState(false)
  const [graphVersion, setGraphVersion] = useState('v20.0')
  const [verifyToken, setVerifyToken] = useState('')
  const [pageAccessToken, setPageAccessToken] = useState('')
  const [recipientId, setRecipientId] = useState('')
  const [statusMsg, setStatusMsg] = useState('')

  const refresh = async () => {
    const res = await fetch(`${API_BASE}/config`)
    const data = await res.json()
    setVerifyTokenSet(data.verify_token_set)
    setPageTokenSet(data.page_access_token_set)
    setGraphVersion(data.graph_api_version)
  }

  useEffect(() => {
    refresh()
  }, [])

  const generateToken = async () => {
    const res = await fetch(`${API_BASE}/token/new`)
    const data = await res.json()
    setVerifyToken(data.verify_token)
  }

  const saveConfig = async () => {
    setStatusMsg('Saving...')
    const res = await fetch(`${API_BASE}/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        verify_token: verifyToken || undefined,
        page_access_token: pageAccessToken || undefined,
        graph_api_version: graphVersion || undefined,
      }),
    })
    await res.json()
    setStatusMsg('Saved')
    refresh()
  }

  const sendTest = async () => {
    if (!recipientId) { setStatusMsg('Enter recipient ID'); return }
    setStatusMsg('Sending...')
    const res = await fetch(`${API_BASE}/test/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ recipient_id: recipientId, text: 'Hello from your AI agent 👋' }),
    })
    const data = await res.json()
    setStatusMsg(data.ok ? 'Sent!' : `Error: ${data.error}`)
  }

  return (
    <div className="card" style={{ marginBottom: '16px' }}>
      <h2 style={{ marginBottom: '12px' }}>Instagram Agent Setup Wizard</h2>
      <div style={{ display: 'grid', gap: '12px' }}>
        <div className="card">
          <h3>Step 1 · Verify Token</h3>
          <p>Status: {verifyTokenSet ? 'Configured' : 'Not set'}</p>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <input placeholder="Verify Token" value={verifyToken} onChange={e => setVerifyToken(e.target.value)} />
            <button className="btn" onClick={generateToken}>Generate</button>
          </div>
        </div>

        <div className="card">
          <h3>Step 2 · Page Access Token</h3>
          <p>Status: {pageTokenSet ? 'Configured' : 'Not set'}</p>
          <input placeholder="Page Access Token" value={pageAccessToken} onChange={e => setPageAccessToken(e.target.value)} />
          <small>Requires permissions: instagram_manage_messages, pages_manage_metadata, pages_messaging</small>
        </div>

        <div className="card">
          <h3>Step 3 · Graph Version</h3>
          <input placeholder="v20.0" value={graphVersion} onChange={e => setGraphVersion(e.target.value)} />
        </div>

        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-primary" onClick={saveConfig}>Save Config</button>
          <span>{statusMsg}</span>
        </div>

        <div className="card">
          <h3>Step 4 · Test Send</h3>
          <input placeholder="Recipient IG user ID" value={recipientId} onChange={e => setRecipientId(e.target.value)} />
          <button className="btn" onClick={sendTest}>Send Test DM</button>
          <small>Use your test IG user ID. Must be connected to the Page.</small>
        </div>

        <div className="card">
          <h3>Step 5 · Webhook</h3>
          <p>Set callback URL to <code>https://YOUR_DOMAIN/webhook</code> and use the Verify Token above.</p>
        </div>
      </div>
    </div>
  )
}