/*
 * @Author: 0x3E5
 * @Date: 2023-02-11 15:11:13
 * @LastEditTime: 2023-02-15 22:21:32
 * @LastEditors: 0x3E5
 * @Description: 
 * @FilePath: \web\src\utils\axios.ts
 */
import axios from 'axios'
import { ERROR_CODE_TYPE } from '@/types/error-code-type'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: '/api',
  timeout: 60000
})

// 请求拦截
service.interceptors.request.use(
  config => {
    // TODO 在此处对发起的请求进行定制化操作
    return config
  },
  err => {
    console.log(err)
    return Promise.reject(err)
  }
)

// 响应拦截
service.interceptors.response.use(
  res => {
    const CODE = res.data['code'] || 200
    if (CODE === 200) {
      return Promise.resolve(res.data)
    } else {
      const MSG =
        ERROR_CODE_TYPE(CODE) || res.data['msg'] || ERROR_CODE_TYPE('default')
      ElMessage.error(MSG)
      return Promise.reject(res.data)
    }
  },
  err => {
    console.log(err)
    let { message } = err
    if (message == 'Network Error') {
      message = '后端接口连接异常'
    } else if (message.includes('timeout')) {
      message = '系统接口请求超时'
    } else if (message.includes('Request failed with status code')) {
      message = `系统接口${message.substr(message.length - 3)}异常`
    }
    ElMessage.error({
      message: message,
      duration: 5 * 1000
    })
    return Promise.reject(err)
  }
)

export default service
