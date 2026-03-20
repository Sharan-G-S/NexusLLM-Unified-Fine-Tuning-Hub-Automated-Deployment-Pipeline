/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0a0c',
        card: 'rgba(23, 23, 26, 0.7)',
        primary: '#3b82f6',
        secondary: '#f43f5e',
        accent: '#8b5cf6',
      },
      backgroundImage: {
        'gradient-mesh': 'radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0, transparent 50%), radial-gradient(at 50% 0%, rgba(139, 92, 246, 0.15) 0, transparent 50%), radial-gradient(at 100% 0%, rgba(244, 63, 94, 0.15) 0, transparent 50%)',
      }
    },
  },
  plugins: [],
}
