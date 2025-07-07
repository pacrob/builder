// @ts-check
import { defineConfig } from 'vite';

// Using dynamic import for better compatibility
export default defineConfig(async () => ({
  root: '.',
  build: {
    outDir: 'dist',
    emptyOutDir: true
  }
}));
