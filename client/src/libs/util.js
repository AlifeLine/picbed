import axios from 'axios'
import { STORAGE_KEY, API_BASEURL } from './vars.js'

export const http = axios.create({
    baseURL: API_BASEURL,
    timeout: 5000,
    withCredentials: false
})

// 添加请求拦截器
http.interceptors.request.use(
    function(config) {
        // 在发送请求之前做些什么
        let token = getStorage('sid')
        if (token) {
            config.headers.Authorization = `Cookie ${token}`
        }
        return config
    },
    function(error) {
        // 对请求错误做些什么
        return Promise.reject(error)
    }
)

// 添加响应拦截器
http.interceptors.response.use(
    function(response) {
        // 对响应数据做点什么
        console.log(response)
        return response
    },
    function(error) {
        // 对响应错误做点什么
        return Promise.reject(error)
    }
)

/**
 * 设置过期存储
 * @param {String} key 索引
 * @param {*} data 数据
 * @param {Number} expire 过期毫秒数，默认0不过期
 */
export function setStorage(key, data, expire = 0) {
    if (key && data) {
        return localStorage.setItem(
            key,
            JSON.stringify({
                exp: expire || 0,
                time: Date.now(),
                data: data
            })
        )
    } else {
        return false
    }
}

export function getStorage(key = STORAGE_KEY) {
    try {
        let obj = JSON.parse(localStorage.getItem(key))
        if (obj && isObject(obj)) {
            let exp = parseInt(obj.exp) || 0,
                time = obj.time,
                data = obj.data
            //如果exp为真则说明有过期时间，否则永久有效直接返回数据
            let now = Date.now()
            if (exp > 0 && now > time + exp) {
                clearStorage(key)
            } else {
                return data
            }
        }
    } catch (e) {
        console.error(e)
    }
}

export function clearStorage(key) {
    return localStorage.removeItem(key)
}

export function isObject(o) {
    return o !== null && typeof o === 'object' && Array.isArray(o) === false
}

export function isValidMap(map) {
    return Array.isArray(map) || isObject(map)
}
