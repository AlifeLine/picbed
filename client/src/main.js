import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import './assets/css/global.css'
import 'element-ui/lib/theme-chalk/index.css'
import router from './router.js'
import store from './store.js'
import { axios } from './util.js'

Vue.use(ElementUI)
Vue.prototype.$http = axios
Vue.prototype.$store = store
Vue.config.productionTip = false

const vm = new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
console.log(vm)
