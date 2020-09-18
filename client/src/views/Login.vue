<template>
    <div class="login-container">
        <el-form
            :model="loginForm"
            :rules="loginRule"
            status-icon
            ref="loginForm"
            label-position="left"
            label-width="0px"
            class="login-area"
        >
            <h3 class="title">登录</h3>
            <el-form-item prop="username">
                <el-input
                    type="text"
                    v-model="loginForm.username"
                    autocomplete="off"
                    placeholder="用户名"
                ></el-input>
            </el-form-item>
            <el-form-item prop="password">
                <el-input
                    type="password"
                    v-model="loginForm.password"
                    autocomplete="off"
                    placeholder="密码"
                    @keyup.enter.native="handleSubmit"
                ></el-input>
            </el-form-item>
            <el-form-item>
                <el-checkbox v-model="checked" class="rememberme">记住我</el-checkbox>
                <el-link type="info" class="forgot" href="https://picbed.pro">忘记密码？</el-link>
            </el-form-item>
            <el-form-item style="width:100%;">
                <el-button
                    type="primary"
                    style="width:100%;"
                    @click="handleSubmit"
                    :loading="logining"
                >登录</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return {
            logining: false,
            loginForm: {
                username: '',
                password: ''
            },
            loginRule: {
                username: [
                    {
                        required: true,
                        message: '请输入用户名',
                        trigger: 'blur'
                    }
                ],
                password: [
                    {
                        required: true,
                        message: '请输入密码',
                        trigger: 'blur'
                    }
                ]
            },
            checked: false
        }
    },
    methods: {
        handleSubmit(event) {
            this.$refs.loginForm.validate((valid) => {
                if (valid) {
                    this.logining = true
                    this.$http
                        .post('/login', {
                            username: this.loginForm.username,
                            password: this.loginForm.password,
                            remember: this.checked
                        })
                        .then((res) => {
                            this.logining = false
                            if (res.data.code === 0) {
                                this.$message.success('登录成功')
                                this.$store.mutations.setLogin(
                                    res.data.sid,
                                    res.data.expire
                                )
                                this.$store.actions.fetchConfig()
                                this.$router.push({ path: '/' })
                            } else {
                                this.$message.info(res.data.msg)
                            }
                        })
                        .catch((e) => {
                            this.logining = false
                            this.$message.error(e)
                        })
                } else {
                    console.log('error submit!')
                    return false
                }
            })
        }
    }
}
</script>

<style scoped>
.login-area {
    -webkit-border-radius: 5px;
    border-radius: 5px;
    margin: 70px auto 30px;
    width: 350px;
    padding: 35px 35px 15px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
}
.login-area .forgot {
    float: right;
}
.login-area .rememberme {
    text-align: left;
    float: left;
}
</style>