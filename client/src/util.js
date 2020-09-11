import axios from 'axios'

axios.defaults.baseURL = process.env.VUE_APP_API_URL || '/api'
axios.defaults.timeout = 5000
axios.defaults.headers.post['Content-Type'] =
    'application/x-www-form-urlencoded'

class Storage {
    constructor(key) {
        this.key = key
        this.obj = localStorage
        if (!this.obj) {
            console.error('不支持localStorage')
            return false
        }
    }

    //设置或跟新本地存储数据
    set(data) {
        if (data) {
            return this.obj.setItem(this.key, JSON.stringify(data))
        }
    }

    //获取本地存储数据
    get() {
        var data = null
        try {
            data = JSON.parse(this.obj.getItem(this.key))
        } catch (e) {
            console.error(e)
        } finally {
            return data
        }
    }

    clear() {
        //清除对象
        return this.obj.removeItem(this.key)
    }
}

function getStorage(key) {
    let s = new Storage(key)
    return s.get()
}

function setStorage(key, data) {
    let s = new Storage(key)
    return s.set(data)
}

function isObject(o) {
    return o !== null && typeof o === 'object' && Array.isArray(o) === false
}

function isValidMap(map) {
    return Array.isArray(map) || isObject(map)
}

export { axios, Storage, getStorage, setStorage, isObject, isValidMap }
