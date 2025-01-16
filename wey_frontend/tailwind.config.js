/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        gray: {
          darkest: '#1f2d3d',
          dark: '#3c4858',
          DEFAULT: '#c0ccda',
          light: '#334155',
          lightest: '#f9fafc',
        },
        surface: {
          0: '#ffffff',
          900: '#121212',
        },
      },
    },
  },
  plugins: [],
};