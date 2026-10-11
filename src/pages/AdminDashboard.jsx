import { useEffect, useState, useContext } from 'react';
import api from '../api/axios';
import { ThemeContext } from '../context/ThemeContext';

export default function AdminDashboard() {
  const [cards, setCards] = useState([]);
  const [filteredCards, setFilteredCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [editingLimit, setEditingLimit] = useState({}); // {cardId: value}
  const { isDark } = useContext(ThemeContext);

  const token = localStorage.getItem('access_token');

  // 1. Fetch All Cards - Admin Only
  const fetchCards = async () => {
    try {
      setLoading(true);
      const res = await api.get('http://localhost:8000/api/admin/cards/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCards(res.data);
      setFilteredCards(res.data);
    } catch (err) {
      setError('Access Denied: Admin only or JWT Expired');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchCards(); }, []);

  // 2. Search Filter
  useEffect(() => {
    const result = cards.filter(c =>
      c.user_email?.toLowerCase().includes(search.toLowerCase()) ||
      c.masked_number?.includes(search) ||
      c.last_4_digits?.includes(search)
    );
    setFilteredCards(result);
  }, [search, cards]);

  // 3. Block / Unblock
  const handleBlockToggle = async (card) => {
    try {
      await api.post(`http://localhost:8000/api/admin/cards/${card.id}/block/`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Optimistic update
      setCards(prev => prev.map(item =>
        item.id === card.id? {...item, is_blocked:!item.is_blocked } : item
      ));
    } catch (err) {
      alert('Failed to update card status');
    }
  };

  // 4. Update Credit Limit
  const handleLimitUpdate = async (cardId) => {
    const newLimit = editingLimit[cardId];
    if (!newLimit || newLimit < 1000) {
      alert('Credit limit must be at least 1000');
      return;
    }
    try {
      await api.patch(`http://localhost:8000/api/admin/cards/${cardId}/`,
        { credit_limit: newLimit },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Limit Updated Successfully');
      fetchCards();
    } catch (err) {
      alert('Limit update failed');
    }
  };

  if (loading) {
    return (
      <div className="p-6 space-y-4">
        <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
      </div>
    );
  }

  if (error) {
    return <div className="p-6 text-center text-red-500 font-bold">{error}</div>;
  }

  return (
    <div className={`p-6 min-h-screen ${isDark? 'bg-gray-900 text-white' : 'bg-gray-50 text-black'}`}>

      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Admin - Card Management</h1>
        <span className="text-sm px-3 py-1 bg-blue-100 text-blue-800 rounded">Total Cards: {cards.length}</span>
      </div>

      {/* Search */}
      <input
        type="text"
        placeholder="Search by user email or last 4 digits..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full p-3 mb-6 rounded border dark:bg-gray-800 dark:border-gray-700 focus:ring-2 focus:ring-blue-500 outline-none"
      />

      {/* Table */}
      <div className="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
        <table className="w-full text-left">
          <thead className="bg-gray-100 dark:bg-gray-700">
            <tr>
              <th className="p-3">User</th>
              <th className="p-3">Card Details</th>
              <th className="p-3">Credit Limit</th>
              <th className="p-3">Activity</th>
              <th className="p-3">Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredCards.map((card) => (
              <tr key={card.id} className="border-t dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                <td className="p-3">
                  <div className="font-medium">{card.user_email}</div>
                  <div className="text-xs text-gray-500">{card.card_type}</div>
                </td>
                <td className="p-3">
                  <div className="font-mono">{card.masked_number}</div>
                  <div className={`text-xs px-2 py-0.5 rounded inline-block mt-1 ${card.is_blocked? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                    {card.is_blocked? 'BLOCKED' : 'ACTIVE'}
                  </div>
                </td>
                <td className="p-3">
                  <div className="flex gap-2">
                    <input
                      type="number"
                      defaultValue={card.credit_limit}
                      onChange={(e) => setEditingLimit({...editingLimit, [card.id]: e.target.value})}
                      className="w-28 p-1 border rounded dark:bg-gray-900"
                    />
                    <button
                      onClick={() => handleLimitUpdate(card.id)}
                      className="px-2 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
                    >
                      Save
                    </button>
                  </div>
                  <div className="text-xs text-gray-500 mt-1">Used: ₹{card.used_limit || 0}</div>
                </td>
                <td className="p-3 text-sm">
                  <div>Txns: {card.transaction_count || 0}</div>
                  <div className="text-xs text-gray-500">Last: {card.last_transaction_date? new Date(card.last_transaction_date).toLocaleDateString() : 'N/A'}</div>
                </td>
                <td className="p-3">
                  <button
                    onClick={() => handleBlockToggle(card)}
                    className={`px-4 py-1.5 rounded font-medium text-sm transition ${card.is_blocked? 'bg-green-600 hover:bg-green-700 text-white' : 'bg-red-600 hover:bg-red-700 text-white'}`}
                  >
                    {card.is_blocked? 'Unblock' : 'Block'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
