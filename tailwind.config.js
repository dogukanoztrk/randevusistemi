/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          950: '#020617',
        },
        app: 'rgba(var(--color-bg-app), <alpha-value>)',
        surface: 'rgba(var(--color-bg-surface), <alpha-value>)',
        'surface-elevated': 'rgba(var(--color-bg-surface-elevated), <alpha-value>)',
        'surface-active': 'rgba(var(--color-bg-surface-active), <alpha-value>)',
        main: 'rgba(var(--color-text-main), <alpha-value>)',
        inverse: 'rgba(var(--color-text-inverse), <alpha-value>)',
        premium: {
          gold: '#C5A059',
          'gold-light': '#D4AF37',
          'gold-dark': '#9A7A40',
          black: '#0A0A0A',
          cream: '#FDFCFB',
          slate: '#1E293B'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Outfit', 'sans-serif'],
      },
      animation: {
        'subtle-pulse': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fade-in 0.6s ease-out forwards',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      },
      boxShadow: {
        'premium': '0 20px 50px -12px rgba(0, 0, 0, 0.05)',
        'premium-hover': '0 30px 60px -15px rgba(0, 0, 0, 0.08)',
        'gold': '0 10px 30px -5px rgba(197, 160, 89, 0.2)',
      }
    },
  },
  plugins: [],
}
