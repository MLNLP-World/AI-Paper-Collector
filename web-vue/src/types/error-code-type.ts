/*
 * @Author: 0x3E5
 * @Date: 2023-02-11 15:00:03
 * @LastEditTime: 2023-02-11 15:03:13
 * @LastEditors: 0x3E5
 * @Description:
 * @FilePath: \web\src\types\error-code-type.ts
 */
export const ERROR_CODE_TYPE = (code: string): string => {
  let errMessage = '未知错误'
  switch (Number(code)) {
    case 400:
      errMessage = '错误的请求'
      break
    case 401:
      errMessage = '未授权，请重新登录'
      break
    case 403:
      errMessage = '拒绝访问'
      break
    case 404:
      errMessage = '请求错误，未找到该资源'
      break
    case 405:
      errMessage = '请求方法未允许'
      break
    case 408:
      errMessage = '请求超时'
      break
    case 500:
      errMessage = '服务器端出错'
      break
    case 501:
      errMessage = '网络未实现'
      break
    case 502:
      errMessage = '网络错误'
      break
    case 503:
      errMessage = '服务不可用'
      break
    case 504:
      errMessage = '网络超时'
      break
    case 505:
      errMessage = 'http版本不支持该请求'
      break
    default:
      errMessage = '其他连接错误'
  }
  return `${code}：${errMessage}`
}
