import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/register/', {
        username,
        password,
        email: email || `${username}@example.com`
      });
      alert('Registered Successfully da!');
      navigate('/login');
    } catch (err) {
      console.error(err.response?.data);
      if (err.response?.data?.error === 'User already exists') {
        alert('User already exists da! Login pannu');
        navigate('/login');
      } else {
        alert('Error: ' + (err.response?.data?.error || 'Registration failed'));
      }
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required /><br/><br/>
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} /><br/><br/>
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required /><br/><br/>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
