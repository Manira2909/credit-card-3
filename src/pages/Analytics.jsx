import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title } from 'chart.js'
import { Pie, Bar } from 'react-chartjs-2'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title)

const Analytics = () => {
  const [data, setData] = useState(null)
  const [search, setSearch] = useState({ min_amount: '', max_amount: '', status: '', page: 1 })
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
    fetchTransactions()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('access')
      const res = await axios.get('http://127.0.0.1:8000/api/analytics/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setData(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const fetchTransactions = async () => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('access')
      const params = new URLSearchParams()
      if (search.min_amount) params.append('min_amount', search.min_amount)
      if (search.max_amount) params.append('max_amount', search.max_amount)
      if (search.status) params.append('status', search.status)

      const res = await axios.get(`http://127.0.0.1:8000/api/transactions/search/?${params}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setTransactions(res.data.results || res.data || [])
    } catch (err) {
      console.error(err)
    }
  }

  const handleExport = async (format) => {
    const token = localStorage.getItem('access_token') || localStorage.getItem('access')
    try {
      const res = await axios.get(`http://127.0.0.1:8000/api/analytics/export/?format=${format}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `analytics.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      window.open(`http://127.0.0.1:8000/api/analytics/export/?format=${format}`, '_blank')
    }
  }

  if (loading) return <div style={{padding:'20px'}}>Loading Analytics...</div>
  if (!data) return <div style={{padding:'20px'}}>No data found. Make some transactions da!</div>

  // SAFE DATA - crash aagathu
  const pieData = {
    labels: data.category_wise?.length? data.category_wise.map(c => c.category || 'Others') : ['No Data'],
    datasets: [{
      data: data.category_wise?.length? data.category_wise.map(c => c.total) : [1],
      backgroundColor: ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40','#E7E9ED']
    }]
  }

  const barData = {
    labels: data.monthly_spending?.length? data.monthly_spending.map(m => `Month ${m.month}`) : ['No Data'],
    datasets: [{ label: 'Spending', data: data.monthly_spending?.length? data.monthly_spending.map(m => m.total) : [0], backgroundColor: '#36A2EB' }]
  }

  return (
    <div style={{padding:'20px', fontFamily:'Arial'}}>
      <h2>📊 Analytics Dashboard</h2>
      <div style={{background:'#f5f5f5', padding:'15px', borderRadius:'8px', marginBottom:'20px'}}>
        <p>Credit Utilization: <b style={{color: data.credit_utilization > 80? 'red' : 'green'}}>{data.credit_utilization?.toFixed(2)}%</b> | Total Spent: <b>₹{data.total_spent}</b></p>
      </div>

      <div style={{display:'flex', gap:'20px', marginTop:'20px', flexWrap:'wrap'}}>
        <div style={{width:'350px', background:'white', padding:'15px', borderRadius:'8px', boxShadow:'0 2px 8px rgba(0,0,0,0.1)'}}>
          <h4>Category Wise</h4>
          <Pie data={pieData} />
        </div>
        <div style={{width:'450px', background:'white', padding:'15px', borderRadius:'8px', boxShadow:'0 2px 8px rgba(0,0,0,0.1)'}}>
          <h4>Monthly Spending</h4>
          <Bar data={barData} />
        </div>
      </div>

      <div style={{marginTop:'30px', background:'white', padding:'15px', borderRadius:'8px', boxShadow:'0 2px 8px rgba(0,0,0,0.1)'}}>
        <h3>🔍 Advanced Search</h3>
        <div style={{display:'flex', gap:'10px', marginBottom:'15px', flexWrap:'wrap'}}>
          <input style={{padding:'8px'}} placeholder="Min Amount" value={search.min_amount} onChange={e=>setSearch({...search, min_amount:e.target.value})} />
          <input style={{padding:'8px'}} placeholder="Max Amount" value={search.max_amount} onChange={e=>setSearch({...search, max_amount:e.target.value})} />
          <select style={{padding:'8px'}} value={search.status} onChange={e=>setSearch({...search, status:e.target.value})}>
            <option value="">All Status</option>
            <option value="SAFE">SAFE</option>
            <option value="FLAGGED">FLAGGED</option>
            <option value="FRAUD">FRAUD</option>
          </select>
          <button style={{padding:'8px 16px', background:'#36A2EB', color:'white', border:'none', borderRadius:'4px', cursor:'pointer'}} onClick={fetchTransactions}>Search</button>
        </div>

        <table border="1" cellPadding="8" style={{width:'100%', borderCollapse:'collapse'}}>
          <thead style={{background:'#f0f0f0'}}><tr><th>Date</th><th>Card</th><th>Merchant</th><th>Amount</th><th>Status</th></tr></thead>
          <tbody>
            {transactions.length > 0? transactions.map(t=>
              <tr key={t.id}>
                <td>{t.date}</td>
                <td>{t.card}</td>
                <td>{t.merchant}</td>
                <td>₹{t.amount}</td>
                <td><span style={{padding:'4px 8px', borderRadius:'4px', background: t.fraud_status==='SAFE'?'#d4edda': t.fraud_status==='FRAUD'?'#f8d7da':'#fff3cd'}}>{t.fraud_status}</span></td>
              </tr>
            ) : <tr><td colSpan="5" style={{textAlign:'center'}}>No transactions found</td></tr>}
          </tbody>
        </table>

        <div style={{marginTop:'20px'}}>
          <button onClick={()=>handleExport('csv')} style={{padding:'10px 20px', marginRight:'10px', background:'#28a745', color:'white', border:'none', borderRadius:'4px', cursor:'pointer'}}>Export CSV</button>
          <button onClick={()=>handleExport('pdf')} style={{padding:'10px 20px', background:'#dc3545', color:'white', border:'none', borderRadius:'4px', cursor:'pointer'}}>Export PDF</button>
        </div>
      </div>
    </div>
  )
}
export default Analytics
