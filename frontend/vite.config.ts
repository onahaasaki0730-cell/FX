import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    strictPort: true,
    cors: true,
    allowedHosts: [
      '5173-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai',
      '.sandbox.novita.ai',
      'localhost',
    ],
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
  preview: {
    port: 5173,
    host: '0.0.0.0',
    strictPort: true,
    cors: true,
    allowedHosts: [
      '5173-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai',
      '.sandbox.novita.ai',
      'localhost',
    ],
  },
})
