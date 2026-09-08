/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#080c14',
          surface: '#0d131f',
          card: '#111827',
          border: '#1f293d',
        },
        quantum: {
          light: '#67e8f9',
          DEFAULT: '#06b6d4',
          dark: '#083344',
          accent: '#8b5cf6',
        },
        clinical: {
          malignant: '#f43f5e',
          benign: '#10b981',
          borderline: '#f59e0b',
          info: '#3b82f6',
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      }
    },
  },
  plugins: [],
}
