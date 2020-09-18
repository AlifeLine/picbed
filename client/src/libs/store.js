import Vue from 'vue'
import { Message } from 'element-ui'
import { STORAGE_KEY } from './vars.js'
import {
    http,
    getStorage,
    setStorage,
    clearStorage,
    isValidMap,
    isObject
} from './util.js'

console.log('init state')
export const state = Vue.observable(
    Object.assign(
        {
            // app state
            isLogin: false,
            isAdmin: false,
            // system config
            icp: '',
            beian: '',
            bg: '',
            bgMobile: '',
            bulletin: '',
            favicon: '',
            logo: '',
            sitename: '',
            // userinfo
            avatar: '',
            email: '',
            nickname: '',
            username: '',
            token: ''
        },
        getStorage()
    )
)
console.log({ ...state })

export const mutations = {
    setLogin(sessionId, expire) {
        state.isLogin = true
        setStorage('sid', sessionId, expire)
    },
    clearLogin() {
        state.isLogin = false
        clearStorage('sid')
    },
    updateLogin: v => (state.isLogin = Boolean(v)),
    changeLogin: () => (state.isLogin = !state.isLogin),
    commit(key, value) {
        state[key] = value
    }
}

export const actions = {
    fetchConfig() {
        //get public config
        http.get('/spa')
            .then(function(res) {
                console.log(res.data)
                Object.keys(res.data).forEach(key => {
                    mutations.commit(key, res.data[key])
                })
                setStorage(STORAGE_KEY, { ...state })
            })
            .catch(function(e) {
                console.error(e)
                Message.error('请求应用配置错误，请刷新重试！')
            })
    }
}

/**
 * 将特定格式的Array|Object转化为Array
 * @param {Array} map 状态字段，可以嵌套Object
 */
function normalizeMap(map) {
    if (isObject(map)) map = [map]
    const ret = []
    for (let item of map) {
        if (isObject(item)) {
            ret.push(...Object.keys(item).map(key => ({ key, val: item[key] })))
        } else {
            ret.push({ key: item, val: item })
        }
    }
    return ret
}

/**
 * 获取需要的状态数据对象
 * @param {String | Array | Object} sts 状态字段
 * @returns {Object}
 */
export const mapState = sts => {
    if (typeof sts === 'string') sts = [sts]
    if (!isValidMap(sts)) throw Error('Invalid type')
    const res = {}
    normalizeMap(sts).forEach(({ key, val }) => {
        res[key] = function mappedState() {
            return typeof val === 'function'
                ? val.call(this, state)
                : state[val]
        }
    })
    return res
}

export default { state, actions, mutations, mapState }
