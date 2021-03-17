// tailwind.config.js
module.exports = {
  theme: {
    ripple: theme => ({
        colors: theme('colors')
    }),
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('tailwindcss-ripple')(),
  ],
}
