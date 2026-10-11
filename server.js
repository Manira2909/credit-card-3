const express = require('express');
const cors = require('cors');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// In-memory data - Dummy Data
let cards = [
  { id: 1, number: '4215 5432 6213 1111', masked: '**** **** **** 1111', holder: 'Niranjana M', expiry: '12/28', cvv: '123', type: 'Visa', balance: 50000 },
  { id: 2, number: '5555 4444 3333 2222', masked: '**** **** **** 2222', holder: 'Niranjana V', expiry: '10/27', cvv: '456', type: 'Mastercard', balance: 75000 }
];

let transactions = [
  { id: 1, cardId: 1, amount: 1500, merchant: 'Amazon', date: '2026-05-13', status: 'Success' },
  { id: 2, cardId: 2, amount: 2500, merchant: 'Flipkart', date: '2026-05-12', status: 'Success' }
];

// Routes

// 1. Root Route
app.get('/', (req, res) => {
  res.send('Backend Running! Credit Card Payment System API is active.');
});

// 2. GET all cards - Supports both /api/cards and /api/cards/
app.get(['/api/cards', '/api/cards/'], (req, res) => {
  res.json(cards);
});

// 3. POST - Add a new card
app.post(['/api/cards', '/api/cards/'], (req, res) => {
  const { number, holder, expiry, cvv, type } = req.body;

  if (!number || !holder || !expiry) {
    return res.status(400).json({ message: 'Missing required fields' });
  }

  const last4 = number.slice(-4);
  const newCard = {
    id: cards.length + 1,
    number: number,
    masked: `**** **** **** ${last4}`,
    holder: holder,
    expiry: expiry,
    cvv: cvv || '123',
    type: type || 'Visa',
    balance: 100000
  };

  cards.push(newCard);
  console.log('New Card Added:', newCard);
  res.status(201).json(newCard);
});

// 4. GET all transactions
app.get(['/api/transactions', '/api/transactions/'], (req, res) => {
  res.json(transactions);
});

// 5. POST - Make a payment
app.post(['/api/pay', '/api/pay/'], (req, res) => {
  const { cardId, amount, merchant } = req.body;

  const newTransaction = {
    id: transactions.length + 1,
    cardId: cardId,
    amount: amount,
    merchant: merchant || 'Test Store',
    date: new Date().toISOString().split('T')[0],
    status: 'Success'
  };

  transactions.push(newTransaction);
  res.status(201).json(newTransaction);
});

// Start Server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});