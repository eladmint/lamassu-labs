import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // Use relative paths for deployment
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@design-system": path.resolve(__dirname, "../../../design-system"),
      "@nuru-ai/design-system": path.resolve(__dirname, "../../../design-system"),
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false, // Disable source maps for production
    cssCodeSplit: true,
    rollupOptions: {
      output: {
        // Ensure consistent file naming
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        manualChunks: {
          vendor: ['react', 'react-dom'],
          charts: ['recharts'],
          ui: ['lucide-react', 'clsx', 'tailwind-merge']
        }
      }
    }
  },
  server: {
    port: 3000,
    host: true
  }
})
