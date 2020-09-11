<template>
    <div class="nav">
        <div class="nav-left">
            <router-link to="/">
                <el-image style="height: 80%" :src="logo"></el-image>
            </router-link>
        </div>
        <div class="nav-right">
            <div v-if="isLogin">
                <el-menu default-active="2" mode="horizontal">
                    <el-menu-item index="1">
                        <el-avatar class="avatar" :src="avatar" :size="30"></el-avatar>
                    </el-menu-item>
                    <el-submenu index="2">
                        <template slot="title">昵称</template>
                        <el-menu-item index="2-1">
                            <i class="saintic-icon saintic-icon-user"></i> 个人资料
                        </el-menu-item>
                        <el-menu-item index="2-2">
                            <i class="saintic-icon saintic-icon-setting"></i> 用户设置
                        </el-menu-item>
                        <el-menu-item index="2-3">
                            <i class="saintic-icon saintic-icon-user-album"></i> 我的图片
                        </el-menu-item>
                        <el-menu-item index="2-4">
                            <i class="saintic-icon saintic-icon-rss"></i> 我的RSS
                        </el-menu-item>
                        <el-menu-item index="2-5" v-show="isAdmin">
                            <i class="saintic-icon saintic-icon-site-manager"></i> 站点管理
                        </el-menu-item>
                        <el-menu-item index="2-6">
                            <i class="saintic-icon saintic-icon-logoff"></i> 登出
                        </el-menu-item>
                    </el-submenu>
                </el-menu>
            </div>
            <div v-else>
                <el-menu mode="horizontal" router>
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
export default {
    name: 'Navbar',
    props: {
        logo: {
            type: String,
            default: require('../assets/img/logo.png')
        },
        avatar: {
            type: String,
            default: require('../assets/img/defaultAvatar.png')
        },
        isLogin: {
            type: Boolean,
            required: true
        },
        isAdmin: Boolean
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