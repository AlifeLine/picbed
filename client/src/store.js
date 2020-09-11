import Vue from 'vue'
import { axios, getStorage, isValidMap, isObject } from './util.js'

export const state = Vue.observable(
    Object.assign(
        {
            // app state
            isLogin: false,
            isAdmin: false,
            sessionId: '',
            // system config
            beian: '',
            bg_mg: '',
            bg_mobile: '',
            bulletin: '',
            favicon: '',
            logo: '',
            site_name: '',
            // userinfo
            avatar: '',
            email: '',
            nickname: '',
            username: ''
        },
        getStorage('picbed-global-state')
    )
)

export const mutations = {
    setLogin: sessionId => {
        state.isLogin = true
        state.sessionId = sessionId
    },
    clearLogin: () => (state.isLogin = false),
    updateLogin: v => (state.isLogin = Boolean(v)),
    changeLogin: () => (state.isLogin = !state.isLogin)
}

export const actions = {
    fetchConfig: () => {
        //axios get public config
        axios
            .get('/spa')
            .then(function(res) {
                console.log(res.data)
                Object.keys(res.data).forEach(key => {
                    state[key] = res.data[key]
                })
            })
            .catch(function(e) {
                console.error(e)
                //show error message on page
            })
    }
}

/**
 * 将特定格式的Array|Object转化为Array
 * @param {Array} map: 状态字段，可以嵌套Object
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
 * @param {String, Array, Object} sts: 状态字段
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
