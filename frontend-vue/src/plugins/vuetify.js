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
          primaryLight: '#f8f8f8',
          secondary: '#402B3A',
          accent: '#D63484',
          error: '#c1121f',
          errorLight: '#edddde',
          errorLight2: '#f2e9e9',
          warning: '#D63484',
          info: '#a78a7f',
          success: '#3D9565',
          successLight: '#ddede4',
          successLight2: '#e9f2ed',
          income: '#dbe6e0',
          expense: '#e4cdcf',
          net: '#e5e5e5',
          selected: '#e6cfdb',
        },
      },
    },
  },
})
