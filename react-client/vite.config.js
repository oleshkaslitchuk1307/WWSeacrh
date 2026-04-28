import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../client',
    emptyOutDir: true
  },
  server: {
    port: 3000,
    proxy: {
      '/users': 'http://127.0.0.1:8000',
      '/auth': 'http://127.0.0.1:8000',
      '/games': 'http://127.0.0.1:8000',
      '/search': 'http://127.0.0.1:8000',
      '/actions': 'http://127.0.0.1:8000',
      '/chat': 'http://127.0.0.1:8000',
      '/sharing': 'http://127.0.0.1:8000',
    }
  }
})
