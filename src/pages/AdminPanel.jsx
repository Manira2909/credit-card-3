import React, { useEffect, useState, useContext } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import { ThemeContext } from '../context/ThemeContext'

const AdminPanel = () => {
  const [cards, setCards] = useState([])
  const navigate = useNavigate()
  const { darkMode, toggleTheme } = useContext(ThemeContext)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) { navigate('/login'); return; }
    axios.get('http://127.0.0.1:8000/api/admin/cards/', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setCards(res.data))
   .catch(err => { alert('Admin only! Login as staff'); navigate('/dashboard') })
  }, [])

  const handleAction = async (id, action) => {
    const token = localStorage.getItem('access_token')
    let payload = { action }
    if (action === 'update_limit') {
      const newLimit = prompt('Enter new limit:')
      if (!newLimit) return
      payload.limit = newLimit
    }
    await axios.post(`http://127.0.0.1:8000/api/admin/cards/${id}/action/`, payload, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert(`${action} success`); window.location.reload()
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Admin Panel</h1>
        <div className="header-actions">
          <button onClick={toggleTheme} className="theme-btn">{darkMode? '☀️' : '🌙'}</button>
          <button onClick={() => navigate('/dashboard')} className="action-btn">Dashboard</button>
        </div>
      </div>
      <table className="admin-table">
        <thead><tr><th>User</th><th>Card</th><th>Limit</th><th>Used</th><th>Status</th><th>Actions</th></tr></thead>
        <tbody>
          {cards.map(c => (
            <tr key={c.id}>
              <td>{c.username}</td>
              <td>{c.masked}</td>
              <td>₹{c.credit_limit}</td>
              <td>₹{c.used_limit}</td>
              <td>{c.is_blocked? '🔴 Blocked' : '🟢 Active'}</td>
              <td>
                <button onClick={() => handleAction(c.id, c.is_blocked? 'unblock' : 'block')} className={`action-btn ${c.is_blocked? 'unblock' : 'block'}`}>{c.is_blocked? 'Unblock' : 'Block'}</button>
                <button onClick={() => handleAction(c.id, 'update_limit')} className="action-btn">Edit Limit</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
export default AdminPanel
