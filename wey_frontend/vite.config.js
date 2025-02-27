import { fileURLToPath, URL } from 'node:url';
import { defineConfig, loadEnv } from 'vite'; // ✅ Ensure env variables are loaded
import vue from '@vitejs/plugin-vue';

export default defineConfig(({ mode }) => {
  // ✅ Load environment variables based on the current mode (e.g., .env, .env.production)
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [vue()],
    server: {
      host: '0.0.0.0', // ✅ Allows access from other devices on your network
      port: 5173,
      strictPort: true, // ✅ Ensures Vite always uses this port
      open: false, // ✅ Prevents auto-opening the browser
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    define: {
      'process.env': env // ✅ Ensures env variables are available globally
    }
  };
});
