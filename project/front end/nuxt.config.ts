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
