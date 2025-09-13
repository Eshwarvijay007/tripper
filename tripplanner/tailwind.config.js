/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#6366f1',
        'primary-purple': '#8b5cf6',
        'primary-purple-2': '#7c3aed',
        'primary-green': '#10b981',
        'accent-green': '#059669',
        'accent-green-2': '#047857',
        'accent-red': '#ef4444',
        'accent-red-2': '#dc2626',
        'background': '#f9fafb',
        'layla-background': '#FFFFFF',
        'layla-foreground': '#000000',
        'layla-muted-foreground': '#71717A',
      },
      fontFamily: {
        'display': ['Inter', 'system-ui', 'sans-serif']
      },
      animation: {
        'fade-in-up': 'fadeInUp 1s ease-out',
        'slide-in': 'slideIn 0.5s ease-out',
        'carousel': 'carousel 20s linear infinite'
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(-50px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' }
        },
        carousel: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-100%)' }
        }
      }
    },
  },
  plugins: [],
}