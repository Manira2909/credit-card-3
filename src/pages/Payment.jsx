import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const Payment = () => {
  const [cardNumber, setCardNumber] = useState('');
  const [amount, setAmount] = useState('');
  const navigate = useNavigate();

  const handlePayment = async (e) => {
    e.preventDefault();
    
    // 16 digit illana error kaatum
    if (cardNumber.length < 4) {
      alert("Please enter valid card number");
      return;
    }

    const last4 = cardNumber.slice(-4);

    try {
      const res = await api.post('/pay/', 
        { 
          card_last4: last4,
          amount: parseFloat(amount) 
        }
      );
      
      alert(`Payment of ₹${amount} Successful!`);
      console.log(res.data);
      navigate('/dashboard'); // success aana piragu dhaan poganum
      
    } catch (err) {
      alert(`Payment Failed: ${err.response?.data?.error || err.message}`);
      console.log(err);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '50px auto', border: '1px solid #ccc', borderRadius: '10px', background: 'white', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px', color: '#333' }}>Credit Card Payment</h2>
      <form onSubmit={handlePayment}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ fontWeight: 'bold' }}>Card Number</label>
          <input 
            type="text" 
            placeholder="4532 1234 5678 9010"
            value={cardNumber}
            onChange={(e) => setCardNumber(e.target.value.replace(/\D/g, ''))} // numbers mattum
            style={{ width: '100%', padding: '10px', marginTop: '5px', borderRadius: '5px', border: '1px solid #ccc' }}
            required
            maxLength="16"
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ fontWeight: 'bold' }}>Amount ₹</label>
          <input 
            type="number" 
            placeholder="Enter amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            style={{ width: '100%', padding: '10px', marginTop: '5px', borderRadius: '5px', border: '1px solid #ccc' }}
            required
            min="1"
          />
        </div>
        <button type="submit" style={{ width: '100%', padding: '12px', background: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '16px', fontWeight: 'bold' }}>
          Pay Now
        </button>
      </form>
    </div>
  );
};

export default Payment;
