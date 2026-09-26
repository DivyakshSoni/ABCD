/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0B0F19', // Deep dark blue-black
        surface: '#151A29', // Slightly lighter dark for cards
        primary: '#3B82F6', // Blue
        secondary: '#8B5CF6', // Purple
        success: '#10B981', // Emerald
        warning: '#F59E0B', // Amber
        danger: '#EF4444', // Red
        textPrimary: '#F3F4F6',
        textSecondary: '#9CA3AF'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
