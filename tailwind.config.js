/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/*.html",
    "./public/assets/*{.js, .css}",
  ],
  theme: {
    extend: {
      letterSpacing: {
        tighter: '-.075em',
        extraWide: '.25em',
      },
      animation: {
        'zoom-image': 'zoom .47s',
      },
      keyframe: {
        'zoom'  : {
          'from' : {
            transform: 'scale(0)',

          },
          'to'   : {
            transform: 'scale(1)',
          },
        },
      }
    },
  },
  plugins: [
  ],
}
