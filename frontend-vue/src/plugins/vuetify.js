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
          primaryLight: '#E7DAE2',
          secondary: '#402B3A',
          accent: '#D63484',
          error: '#c1121f',
          warning: '#D63484',
          info: '#a78a7f',
          success: '#3D9565',
        },
      },
    },
  },
})
