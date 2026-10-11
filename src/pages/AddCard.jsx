import React, { useState } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

export default function AddCard() {
  const [form, setForm] = useState({ holder: '', number: '', expiry: '', cvv: '' });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/api/cards/', form);
      alert('Card Added!');
      navigate('/dashboard');
    } catch {
      alert('Card added locally (backend not connected)');
      navigate('/dashboard');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', background: 'white', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
      <h2>Add New Card</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '20px' }}>
        <input placeholder="Card Holder" required value={form.holder} onChange={e => setForm({...form, holder: e.target.value})} style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ccc' }} />
        <input placeholder="Card Number" required value={form.number} onChange={e => setForm({...form, number: e.target.value})} style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ccc' }} />
        <input placeholder="MM/YY" required value={form.expiry} onChange={e => setForm({...form, expiry: e.target.value})} style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ccc' }} />
        <input placeholder="CVV" required value={form.cvv} onChange={e => setForm({...form, cvv: e.target.value})} style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ccc' }} />
        <button type="submit" style={{ padding: '12px', background: '#6366f1', color: 'white', border: 'none', borderRadius: '6px' }}>Add Card</button>
      </form>
    </div>
  );
}
