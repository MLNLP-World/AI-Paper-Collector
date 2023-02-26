/*
 * @Author: 0x3E5
 * @Date: 2023-02-11 13:48:18
 * @LastEditTime: 2023-02-11 16:13:17
 * @LastEditors: 0x3E5
 * @Description: 
 * @FilePath: \web\src\main.ts
 */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementIcons from './icons/element-icons'
import 'element-plus/theme-chalk/dark/css-vars.css'
import 'element-plus/theme-chalk/el-loading.css'
import 'element-plus/theme-chalk/el-message.css'

import './assets/main.css'

const app = createApp(App)

app.use(router)
app.use(ElementIcons)
app.mount('#app')
