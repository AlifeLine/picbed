<template>
    <div class="nav">
        <div class="nav-left">
            <router-link to="/">
                <el-image style="height: 80%" :src="logo"></el-image>
            </router-link>
        </div>
        <div class="nav-right">
            <div v-if="isLogin">
                <el-menu mode="horizontal" router :default-active="this.$route.path">
                    <el-menu-item index>
                        <el-avatar class="avatar" :src="avatar" :size="30"></el-avatar>
                    </el-menu-item>
                    <el-submenu index="/control" v-if="isControl()">
                        <template slot="title">{{ name }}</template>
                        <el-menu-item index="/control/setting">
                            <i class="saintic-icon saintic-icon-system-setting"></i> 配置管理
                        </el-menu-item>
                        <el-menu-item index="/control/hook">
                            <i class="saintic-icon saintic-icon-plugin"></i> 钩子扩展
                        </el-menu-item>
                        <el-menu-item index="/control/user">
                            <i class="saintic-icon saintic-icon-user-manager"></i> 用户管理
                        </el-menu-item>
                        <el-menu-item>-------------</el-menu-item>
                        <el-menu-item index="/user">
                            <i class="saintic-icon saintic-icon-home"></i> 个人中心
                        </el-menu-item>
                        <el-menu-item index="/logout">
                            <i class="saintic-icon saintic-icon-logoff"></i> 登出
                        </el-menu-item>
                    </el-submenu>
                    <el-submenu index="/user" v-else>
                        <template slot="title">{{ name }}</template>
                        <el-menu-item index="/user/profile">
                            <i class="saintic-icon saintic-icon-user"></i> 个人资料
                        </el-menu-item>
                        <el-menu-item index="/user/setting">
                            <i class="saintic-icon saintic-icon-setting"></i> 用户设置
                        </el-menu-item>
                        <el-menu-item index="/user/image">
                            <i class="saintic-icon saintic-icon-user-album"></i> 我的图片
                        </el-menu-item>
                        <el-menu-item index="/user/feed">
                            <i class="saintic-icon saintic-icon-rss"></i> 我的RSS
                        </el-menu-item>
                        <el-menu-item>-------------</el-menu-item>
                        <el-menu-item index="/control" v-if="isAdmin">
                            <i class="saintic-icon saintic-icon-site-manager"></i> 站点管理
                        </el-menu-item>
                        <el-menu-item index="/logout">
                            <i class="saintic-icon saintic-icon-logoff"></i> 登出
                        </el-menu-item>
                    </el-submenu>
                </el-menu>
            </div>
            <div v-else>
                <el-menu mode="horizontal" router :default-active="this.$route.path">
                    <el-menu-item index="/login">
                        <i class="saintic-icon saintic-icon-login"></i> 登录
                    </el-menu-item>
                    <el-menu-item index="/register">
                        <i class="saintic-icon saintic-icon-register"></i> 注册
                    </el-menu-item>
                </el-menu>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState } from '@/libs/store.js'
export default {
    name: 'Navbar',
    computed: {
        name() {
            return this.nickname || this.username
        },
        logo() {
            return this.$store.state.logo || require('../assets/img/logo.png')
        },
        avatar() {
            return (
                this.$store.state.avatar ||
                require('../assets/img/defaultAvatar.png')
            )
        },
        ...mapState(['isLogin', 'isAdmin', 'nickname', 'username'])
    },
    methods: {
        isControl() {
            return this.isAdmin && this.$route.path.startsWith('/control')
        }
    }
}
</script>

<style>
.nav {
    height: 60px;
    position: relative;
    border-radius: 2px;
    font-size: 15px;
    box-sizing: border-box;
}
.nav .nav-left {
    position: absolute;
    left: 0;
    top: 0;
    width: 200px;
}
.nav .nav-right {
    position: absolute;
    right: 0;
    top: 0;
}
.nav .nav-right .avatar {
    background: #fff;
}
</style>