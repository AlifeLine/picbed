<template>
    <div id="app">
        <el-container>
            <el-header>
                <Navbar />
            </el-header>
            <el-main>
                <router-view />
            </el-main>
            <el-footer>
                <Footer />
            </el-footer>
        </el-container>
    </div>
</template>

<script>
import { STORAGE_KEY } from '@/libs/vars.js'
import { setStorage } from '@/libs/util.js'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
console.log('init app.vue')

export default {
    name: 'App',
    components: {
        Navbar,
        Footer
    },
    created() {
        //获取全局基本配置
        this.$store.actions.fetchConfig()
        //在页面刷新时将状态数据保存到Storage
        window.addEventListener('beforeunload', (e) => {
            setStorage(STORAGE_KEY, { ...this.$store.state })
            e.returnValue = ''
        })
    }
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
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
