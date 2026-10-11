import axios from 'axios'

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
})

API.interceptors.request.use((req) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    req.headers.Authorization = `Bearer ${token}`
  }
  return req
})

export const login = (data) => API.post('auth/login/', data)
export const register = (data) => API.post('auth/register/', data)
export const getDashboard = () => API.get('dashboard/summary')
export const getCards = () => API.get('cards/')

export default API
