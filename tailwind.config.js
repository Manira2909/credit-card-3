import { useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}


function Header(){
  const {isDark, toggleTheme} = useContext(ThemeContext);
  return <button onClick={toggleTheme} className="p-2 rounded bg-gray-200 dark:bg-gray-800">
    {isDark? '☀️ Light' : '🌙 Dark'}
  </button>
}
