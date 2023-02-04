/** @type {import('tailwindcss').Config} */
module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: {
      enabled: false, //true for production build
      content: [
          '../**/templates/*.html',
          '../**/templates/**/*.html',
          '../properties/templates/index.html'
      ]
  },
  theme: {
      extend: {
        backgroundImage: {
          'map': "url('../static/mapImg.jpg')"
        }
      },
  },
  variants: {},
  plugins: [],
}
