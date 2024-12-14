import path from 'path';
import { defineConfig } from 'vite'
import autoprefixer from 'autoprefixer'
import tailwind from 'tailwindcss'
import vue from '@vitejs/plugin-vue'
import svgLoader from 'vite-svg-loader';

// https://vite.dev/config/
export default defineConfig({
  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer()],
    },
  },
  plugins: [vue(),  svgLoader()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // Maps '@' to the 'src' directory
    },
  }
})
