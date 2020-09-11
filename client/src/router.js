import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from './views/Index.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Index',
        component: Index
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('./views/Login.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('./views/Register.vue')
    }
]

const router = new VueRouter({
    routes
})

export default router
