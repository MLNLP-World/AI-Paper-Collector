/*
 * @Author: 0x3E5
 * @Date: 2023-02-12 16:16:30
 * @LastEditTime: 2023-02-12 16:27:43
 * @LastEditors: 0x3E5
 * @Description:
 * @FilePath: \web\src\api\paper.ts
 */
import request from '@/utils/axios'

// paper search
export const paperSearch = (params: Object) =>
  request({
    url: '/search',
    method: 'get',
    params
  })

// guess your like
export const guessYourLike = (params: Object) =>
  request({
    url: '/get_guess_you_like',
    method: 'get',
    params
  })
