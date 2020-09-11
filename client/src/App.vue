<template>
    <div id="app">
        <el-container>
            <el-header>
                <Navbar :isLogin="isLogin" />
            </el-header>
            <el-main>
                <router-view />
            </el-main>
            <el-footer>
                <Footer :icp="icp" :beian="beian" />
            </el-footer>
        </el-container>
    </div>
</template>

<script>
import { actions, mutations, mapState } from './store.js'
import { Storage } from './util.js'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

export default {
    name: 'App',
    components: {
        Navbar,
        Footer
    },
    computed: mapState(['icp', 'beian', 'isLogin']),
    created() {
        //获取全局基本配置
        actions.fetchConfig()
        //在页面刷新时将状态数据保存到Storage里
        window.addEventListener('beforeunload', e => {
            const pgs = new Storage('picbed-global-state')
            pgs.set({ ...this.$store.state })
            e.returnValue = ''
        })
    },
    methods: {
        changeLogin() {
            mutations.changeLogin()
            console.log(this.$store.state.isLogin)
        }
    }
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}
body > .el-container {
    margin-bottom: 40px;
}
.el-header,
.el-footer {
    line-height: 60px;
}
</style>
