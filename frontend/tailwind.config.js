/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        techno: {
          primary: '#ff006e',
          secondary: '#8338ec',
          accent: '#3a86ff',
          dark: '#0a0a0a',
          darker: '#000000',
          light: '#ffffff',
          gray: '#333333',
          'gray-light': '#666666',
        },
      },
      fontFamily: {
        sans: ['var(--font-geist-sans)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-geist-mono)', 'monospace'],
      },
      animation: {
        'pulse-techno': 'pulse-techno 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        glow: 'glow 2s ease-in-out infinite',
      },
      keyframes: {
        'pulse-techno': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
        glow: {
          '0%, 100%': { boxShadow: '0 0 5px var(--techno-primary)' },
          '50%': { boxShadow: '0 0 20px var(--techno-primary), 0 0 30px var(--techno-primary)' },
        },
      },
    },
  },
  plugins: [],
}
