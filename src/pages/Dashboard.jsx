import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedCard, setSelectedCard] = useState(null);
  const [amount, setAmount] = useState('');
  const [payMsg, setPayMsg] = useState('');
  const navigate = useNavigate();

  const fetchDashboard = async () => {
    const token = localStorage.getItem('access');
    if (!token) {
      setError('No token found da! Login pannu first!');
      setLoading(false);
      setTimeout(() => navigate('/login'), 1000);
      return;
    }
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/dashboard/summary/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setData(res.data);
      // Fetch transactions also
      const txnRes = await axios.get('http://127.0.0.1:8000/api/transactions/list/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTransactions(txnRes.data.results || txnRes.data || []);
      setLoading(false);
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Unauthorized da! Token expire!');
        localStorage.clear();
        setTimeout(() => navigate('/login'), 1500);
      } else {
        setError('Error: ' + (err.response?.data?.error || err.message));
      }
      setLoading(false);
    }
  };

  useEffect(() => { fetchDashboard(); }, []);

  const handlePay = async () => {
    if (!amount || isNaN(amount)) { setPayMsg('Valid amount enter pannu da!'); return; }
    const token = localStorage.getItem('access');
    try {
      await axios.post('http://127.0.0.1:8000/api/transactions/', {
        card_id: selectedCard.id,
        amount: parseFloat(amount),
        merchant: 'Test Payment'
      }, { headers: { Authorization: `Bearer ${token}` } });
      setPayMsg('Payment Success da! 🎉');
      setAmount('');
      setTimeout(() => { setSelectedCard(null); setPayMsg(''); fetchDashboard(); }, 1000);
    } catch (err) {
      setPayMsg('Failed da: ' + (err.response?.data?.error || JSON.stringify(err.response?.data) || err.message));
    }
  };

  const handleLogout = () => { localStorage.clear(); navigate('/login'); };

  if (loading) return <div style={{ padding: '50px', textAlign: 'center' }}><h2>Loading da...</h2></div>;
  if (error) return <div style={{ padding: '50px', textAlign: 'center', color: 'red' }}><h2>{error}</h2><button onClick={() => navigate('/login')}>Go to Login</button></div>;

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>💳 Credit Card Dashboard</h2>
        <div style={{display:'flex', gap:'10px'}}>
          <button onClick={()=>navigate('/analytics')} style={{ padding: '8px 16px', background: '#667eea', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Analytics</button>
          <button onClick={handleLogout} style={{ padding: '8px 16px', background: 'red', color: 'white', border: 'none',borderRadius: '5px', cursor: 'pointer' }}>Logout</button>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '20px', marginTop:'20px', flexWrap:'wrap' }}>
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '10px', minWidth: '200px', background: '#f0f8ff' }}><h3>Total Cards</h3><h1>{data?.total_cards || 0}</h1></div>
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '10px', minWidth: '200px', background: '#fff8dc' }}><h3>Total Used</h3><h1>₹{data?.total_balance?.toFixed(2) || 0}</h1></div>
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '10px', minWidth: '200px', background: '#ffe4e1' }}><h3>Utilization</h3><h1>{data?.credit_utilization?.toFixed(1) || 0}%</h1></div>
      </div>

      <h3 style={{ marginTop: '30px' }}>Your Cards (Click to Pay):</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '15px' }}>
        {data?.cards?.map((card) => (
          <div key={card.id} onClick={()=>setSelectedCard(card)} style={{ border: '2px solid #333', padding: '15px', borderRadius: '15px', background: card.blocked? '#ffcccc' : 'linear-gradient(135deg, #667eea, #764ba2)', color: card.blocked? 'black' : 'white', cursor:'pointer' }}>
            <p style={{ fontSize: '18px', fontWeight: 'bold'}}>{card.masked}</p>
            <p>Limit: ₹{card.limit}</p>
            <p>Used: ₹{card.used}</p>
            <p>Status: {card.blocked? '🔴 BLOCKED' : '🟢ACTIVE'}</p>
            <p style={{fontSize:'12px', marginTop:'10px', background:'rgba(0,0,0,0.2)', padding:'5px', borderRadius:'5px'}}>👆 Click to make payment</p>
          </div>
        ))}
      </div>

      <div style={{marginTop:'40px', background:'white', padding:'20px', borderRadius:'10px', boxShadow:'0 2px 8px rgba(0,0,0,0.1)'}}>
        <h3>💸 Recent Transactions</h3>
        <table style={{width:'100%', borderCollapse:'collapse', marginTop:'10px'}} border="1" cellPadding="10">
          <thead style={{background:'#f0f0f0'}}><tr><th>Date</th><th>Card</th><th>Merchant</th><th>Amount</th><th>Status</th></tr></thead>
          <tbody>
            {transactions.length > 0? transactions.slice(0,10).map(t=>(
              <tr key={t.id}>
                <td>{t.date}</td>
                <td>{t.card_last4 || t.card}</td>
                <td>{t.merchant}</td>
                <td>₹{t.amount}</td>
                <td><span style={{padding:'4px 8px', borderRadius:'4px', background: t.fraud_status==='SAFE'?'#d4edda':'#fff3cd', color: t.fraud_status==='SAFE'?'#155724':'#856404'}}>{t.fraud_status}</span></td>
              </tr>
            )) : <tr><td colSpan="5" style={{textAlign:'center'}}>No transactions yet da! Pay pannu!</td></tr>}
          </tbody>
        </table>
        {transactions.length > 10 && <p style={{marginTop:'10px', textAlign:'center'}}><a href="#" onClick={(e)=>{e.preventDefault(); navigate('/analytics')}}>View All in Analytics →</a></p>}
      </div>

      {selectedCard && (
        <div style={{position:'fixed', top:0, left:0, right:0, bottom:0, background:'rgba(0,0,0,0.5)', display:'flex', justifyContent:'center', alignItems:'center', zIndex:1000}}>
          <div style={{background:'white', padding:'30px', borderRadius:'15px', minWidth:'350px'}}>
            <h3>Pay with {selectedCard.masked}</h3>
            <p>Available: ₹{selectedCard.limit - selectedCard.used}</p>
            <input type="number" placeholder="Amount" value={amount} onChange={(e)=>setAmount(e.target.value)} style={{width:'100%', padding:'10px', margin:'10px 0', borderRadius:'5px', border:'1px solid #ddd'}}/>
            {payMsg && <p style={{color: payMsg.includes('Success')?'green':'red'}}>{payMsg}</p>}
            <div style={{display:'flex', gap:'10px', marginTop:'10px'}}>
              <button onClick={handlePay} style={{flex:1, padding:'10px', background:'#667eea', color:'white', border:'none', borderRadius:'5px', cursor:'pointer'}}>Pay Now</button>
              <button onClick={()=>{setSelectedCard(null); setAmount(''); setPayMsg('')}} style={{flex:1, padding:'10px',background:'#ccc', border:'none', borderRadius:'5px', cursor:'pointer'}}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
export default Dashboard;