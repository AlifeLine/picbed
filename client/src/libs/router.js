import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '@/views/Index.vue'
import { mutations } from './store.js'

console.log('init router')

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
        component: () => import('@/views/Login.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/views/Register.vue')
    },
    {
        path: '/logout',
        name: 'Logout',
        redirect() {
            mutations.clearLogin()
            return '/'
        },
        meta: { requiresAuth: true }
    },
    {
        path: '/control',
        name: 'Control',
        component: () => import('@/views/admin/Control.vue'),
        children: [
            {
                path: 'setting',
                component: () => import('@/views/admin/AdminSetting.vue')
            },
            {
                path: 'hook',
                component: () => import('@/views/admin/AdminHook.vue')
            },
            {
                path: 'user',
                component: () => import('@/views/admin/AdminUser.vue')
            }
        ]
    },
    {
        path: '/user',
        name: 'Home',
        component: () => import('@/views/user/Home.vue'),
        children: [
            {
                path: 'profile',
                component: () => import('@/views/user/UserProfile.vue')
            },
            {
                path: 'setting',
                component: () => import('@/views/user/UserSetting.vue')
            },
            {
                path: 'image',
                component: () => import('@/views/user/UserImage.vue')
            }
        ]
    }
]

const router = new VueRouter({
    mode: 'history',
    routes
})

/*
router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // this route requires auth, check if logged in
        // if not, redirect to login page.
        if (!auth.loggedIn()) {
            next({
                path: '/login',
                query: { redirect: to.fullPath }
            })
        } else {
            next()
        }
    } else {
        next() // 确保一定要调用 next()
    }
})
*/
export default router
