import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [logs, setLogs] = useState([])

  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/logs')

    ws.onmessage = (event) => {
      const log = JSON.parse(event.data)
      setLogs((prevLogs) => [log, ...prevLogs].slice(0, 50)) // keep latest 50
    }

    ws.onerror = (err) => {
      console.error('WebSocket error:', err)
    }

    return () => ws.close()
  }, [])

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace', backgroundColor: '#0d1117', color: '#c9d1d9', minHeight: '100vh' }}>
      <h1>🛡️ AI SOC Agent — Live Log Feed</h1>
      <p>Total logs received: {logs.length}</p>

      <div>
        {logs.map((log, index) => (
          <div
            key={index}
            style={{
              padding: '8px',
              marginBottom: '4px',
              borderRadius: '4px',
              backgroundColor: log.is_attack_injected ? '#3d1a1a' : '#161b22',
              borderLeft: log.is_attack_injected ? '4px solid red' : '4px solid green'
            }}
          >
            <strong>{log.is_attack_injected ? `⚠️ ATTACK (${log.attack_type})` : '✅ normal'}</strong>
            {' | '}src: {log.src_ip}
            {' | '}service: {log.service}
            {' | '}flag: {log.flag}
            {' | '}{new Date(log.timestamp).toLocaleTimeString()}
          </div>
        ))}
      </div>
    </div>
  )
}

export default App