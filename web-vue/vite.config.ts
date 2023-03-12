/*
 * @Author: 0x3E5
 * @Date: 2023-03-11 23:10:13
 * @LastEditTime: 2023-03-11 23:24:32
 * @LastEditors: 0x3E5
 * @Description: vite config file
 * @FilePath: \AI-Paper-Collector\web-vue\vite.config.ts
 */
import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import { compression } from 'vite-plugin-compression2'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  const ENV = loadEnv(mode, process.cwd(), '')
  return {
    base: './',
    envPrefix: ['VITE', 'VUE'],
    plugins: [
      vue(),
      vueJsx(),
      AutoImport({
        resolvers: [ElementPlusResolver()]
      }),
      Components({
        resolvers: [ElementPlusResolver()]
      }),
      compression()
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      host: '0.0.0.0',
      port: 8080,
      strictPort: true,
      open: false,
      proxy: {
        '/api': {
          target: ENV.VUE_APP_BASE_URL,
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, '/')
        }
        // '/socket.io': {
        //   target: 'ws://localhost:3000',
        //   ws: true,
        // },
      }
    },
    build: {
      outDir: '../static',
      emptyOutDir: true
    }
  }
})
