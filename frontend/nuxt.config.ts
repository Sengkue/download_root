// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  // Enable Nuxt 4 compatibility features
  future: {
    compatibilityVersion: 4,
  },

  runtimeConfig: {
    public: {
      openRouterApiKey: process.env.NUXT_PUBLIC_OPENROUTER_API_KEY || '',
    }
  },

  app: {
    head: {
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Noto+Sans+Lao:wght@300;400;500;600;700;800;900&family=Outfit:wght@400;500;600;700&display=swap'
        }
      ]
    }
  },

  devtools: { enabled: false },

  build: {
    transpile: ['vuetify'],
  },

  modules: [
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
    //...
  ],

  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },

  compatibilityDate: '2024-11-01',
})
