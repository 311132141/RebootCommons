/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        gmarket: ['GmarketSans', 'sans-serif'], // Use the custom font
      },
      fontWeight: {
        light: 300,
        medium: 500,
        bold: 700,
      },
      fontSize: {
        'heading-h1-sm': ['2rem', { lineHeight: '2.5rem' }], // Mobile: 32px/40px
        'heading-h1-md': ['3rem', { lineHeight: '3.5rem' }], // Tablet: 48px/56px
        'heading-h1-lg': ['3.75rem', { lineHeight: '4.5rem' }], // Desktop: 60px/72px

        'heading-h2-sm': ['1.75rem', { lineHeight: '2rem' }], // Mobile: 28px/32px
        'heading-h2-md': ['2.5rem', { lineHeight: '3rem' }], // Tablet: 40px/48px
        'heading-h2-lg': ['3rem', { lineHeight: '3.5rem' }], // Desktop: 48px/56px

        'heading-h3-sm': ['1.5rem', { lineHeight: '1.75rem' }], // Mobile: 24px/28px
        'heading-h3-md': ['2rem', { lineHeight: '2.5rem' }], // Tablet: 32px/40px
        'heading-h3-lg': ['2.5rem', { lineHeight: '3rem' }], // Desktop: 40px/48px

        'heading-h4-sm': ['1.5rem', { lineHeight: '1.75rem' }], // Mobile: 24px/28px
        'heading-h4-md': ['1.75rem', { lineHeight: '2rem' }], // Tablet: 28px/32px
        'heading-h4-lg': ['2rem', { lineHeight: '2.5rem' }], // Desktop: 32px/40px

        'heading-h5-sm': ['1.25rem', { lineHeight: '1.5rem' }], // Mobile: 20px/24px
        'heading-h5-md': ['1.5rem', { lineHeight: '1.75rem' }], // Tablet: 24px/28px
        'heading-h5-lg': ['1.5rem', { lineHeight: '1.75rem' }], // Desktop: 24px/28px

        'heading-h6-sm': ['1.25rem', { lineHeight: '1.5rem' }], // Mobile: 20px/24px
        'heading-h6-md': ['1.25rem', { lineHeight: '1.5rem' }], // Tablet: 20px/24px
        'heading-h6-lg': ['1.25rem', { lineHeight: '1.5rem' }], // Desktop: 20px/24px

        'body-sm': ['0.75rem', { lineHeight: '1.25rem' }], // 12px font size, 20px line height
        'body-md': ['1rem', { lineHeight: '1.5rem' }],     // 16px font size, 24px line height
        'body-lg': ['1.25rem', { lineHeight: '2rem' }],    // 20px font size, 32px line height
      },
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
      lineHeight: {
        heading: {
          h1: '4.5rem', // 72px
          h2: '3.5rem', // 56px
          h3: '3rem',   // 48px
          h4: '2.5rem', // 40px
          h5: '1.75rem', // 28px
          h6: '1.5rem',  // 24px
        },
        body: {
          sm: '1.25rem', // 20px
          md: '1.5rem',  // 24px
          lg: '2rem',    // 32px
        },
      },
      spacing: {
        'paragraph-h1': '3rem', // 48px
        'paragraph-h2': '2.5rem', // 40px
        'paragraph-h3': '2.25rem', // 36px
        'paragraph-h4': '2rem', // 32px
        'paragraph-h5': '1.75rem', // 28px
        'paragraph-h6': '1.75rem', // 28px

        'paragraph-body-sm': '1rem', // 16px
        'paragraph-body-md': '1rem', // 16px
        'paragraph-body-lg': '1.25rem', // 20px
      },
    },
    screens: {
      sm: '640px', // Mobile
      md: '768px', // Tablet
      lg: '1024px', // Desktop
    },
  },
  plugins: [],
};