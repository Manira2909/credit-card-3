import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const logout = () => {
    localStorage.removeItem('token')
    navigate('/')
  }
  return (
    <nav className="bg-white shadow px-6 py-4 flex justify-between items-center">
      <Link to="/dashboard" className="text-xl font-bold text-indigo-600">PaySecure</Link>
      <div className="flex gap-4 items-center">
        <Link to="/dashboard" className="text-gray-700 hover:text-indigo-600 font-medium">Dashboard</Link>
        <Link to="/add-card" className="text-gray-700 hover:text-indigo-600 font-medium">Add Card</Link>
        <Link to="/pay" className="text-gray-700 hover:text-indigo-600 font-medium">Pay</Link>
        <button onClick={logout} className="bg-red-500 text-white px-4 py-1.5 rounded-lg text-sm font-semibold">Logout</button>
      </div>
    </nav>
  )
}
