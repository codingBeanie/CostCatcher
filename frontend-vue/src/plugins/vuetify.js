// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'myTheme',
    themes: {
      myTheme: {
        colors: {
          primary: '#F8F4EC',
          secondary: '#402B3A',
          accent: '#D63484',
          error: '#D63484',
          warning: '#D63484',
          info: '#c0c2c0',
          success: '#97c98d',
        },
      },
    },
  },
})
