/*
 * @Author: 0x3E5
 * @Date: 2023-02-11 15:42:00
 * @LastEditTime: 2023-02-11 15:42:15
 * @LastEditors: 0x3E5
 * @Description: 全局注册element图标
 * @FilePath: \web\src\icons\element-icons.ts
 */
import type { App } from 'vue'
import * as icons from '@element-plus/icons-vue'
export default {
  install: (app: App<Element>) => {
    for (const [key, component] of Object.entries(icons)) {
      app.component(key, component)
    }
  }
}
