import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // localhost illama 127.0.0.1 podu
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access'); // <-- 'jwt' illama 'access'
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access'); // <-- 'jwt' illama 'access'
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
