import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    theme: {
      defaultTheme: 'vocabLight',
      themes: {
        vocabLight: {
          dark: false,
          colors: {
            background: '#fbf9f5',
            surface: '#fbf9f5',
            'on-surface': '#1b1c1a',
            'on-surface-variant': '#43474e',
            'surface-container': '#efeeea',
            'surface-container-low': '#f5f3ef',
            'surface-container-lowest': '#ffffff',
            'surface-container-highest': '#e4e2de',
            primary: '#002045',
            'on-primary': '#ffffff',
            'primary-container': '#1a365d',
            'on-primary-container': '#86a0cd',
            'primary-fixed': '#d6e3ff',
            secondary: '#b6005a',
            'on-secondary': '#ffffff',
            'secondary-container': '#df1a72',
            'on-secondary-container': '#fffbff',
            'secondary-fixed': '#ffd9e1',
            tertiary: '#002522',
            'on-tertiary': '#ffffff',
            'tertiary-container': '#003d38',
            'on-tertiary-container': '#56ada3',
            'tertiary-fixed': '#9cf2e8',
            error: '#ba1a1a',
            'on-error': '#ffffff',
            'error-container': '#ffdad6',
            'on-error-container': '#93000a',
            white: '#ffffff',
            'on-white': '#1b1c1a',
          }
        }
      }
    }
  })
  app.vueApp.use(vuetify)
})
