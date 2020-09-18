<template>
    <div class="register-container">
        <el-form
            :model="registerForm"
            :rules="registerRule"
            ref="registerForm"
            label-position="left"
            label-width="0px"
            class="register-area"
        >
            <h3 class="title">注册</h3>
            <el-form-item prop="username">
                <el-input
                    type="text"
                    v-model="registerForm.username"
                    autocomplete="off"
                    placeholder="请输入用户名"
                ></el-input>
            </el-form-item>
            <el-form-item v-if="visible" prop="password">
                <el-input
                    type="password"
                    v-model="registerForm.password"
                    placeholder="请输入密码"
                    autocomplete="off"
                >
                    <i
                        slot="suffix"
                        title="显示密码"
                        @click="changePass"
                        style="cursor:pointer;"
                        class="saintic-icon saintic-icon-eye-open"
                    ></i>
                </el-input>
            </el-form-item>
            <el-form-item v-else prop="password">
                <el-input
                    type="text"
                    v-model="registerForm.password"
                    placeholder="请输入密码"
                    autocomplete="off"
                >
                    <i
                        slot="suffix"
                        title="隐藏密码"
                        @click="changePass"
                        style="cursor:pointer;"
                        class="saintic-icon saintic-icon-eye-close"
                    ></i>
                </el-input>
            </el-form-item>
            <el-form-item>
                <el-checkbox v-model="checked" class="agree" prop="agree" required>
                    我同意
                    <el-link type="primary" @click="showTerms">服务条款</el-link>和
                    <el-link type="primary" @click="showPrivacy">隐私政策</el-link>
                </el-checkbox>
            </el-form-item>
            <el-form-item style="width:100%;">
                <el-button
                    type="primary"
                    style="width:100%;"
                    @click="handleSubmit"
                    :loading="registering"
                >注册</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
export default {
    name: 'Register',
    data() {
        return {
            registering: false,
            registerForm: {
                username: '',
                password: ''
            },
            registerRule: {
                username: [
                    {
                        required: true,
                        message: '请输入用户名',
                        trigger: 'blur'
                    },
                    {
                        min: 4,
                        max: 32,
                        message: '用户名要求4-32位字符',
                        trigger: 'blur'
                    },
                    {
                        pattern: /^[a-zA-Z][0-9a-zA-Z\_]{3,31}$/,
                        message: '用户名要求以字母开头加字母、数字或下划线',
                        trigger: 'blur'
                    }
                ],
                password: [
                    {
                        required: true,
                        message: '请输入密码',
                        trigger: 'blur'
                    },
                    {
                        pattern: /^[\S]{6,32}$/,
                        message: '密码要求6到32位且无空格',
                        trigger: 'blur'
                    }
                ]
            },
            checked: false,
            visible: true
        }
    },
    methods: {
        changePass() {
            this.visible = !this.visible
        },
        handleSubmit(event) {
            this.$refs.registerForm.validate(valid => {
                if (!this.checked) {
                    return this.$message.error('注册需同意服务条款与隐私政策')
                }
                if (valid) {
                    this.registering = true
                    this.$http
                        .post('/register', {
                            username: this.registerForm.username,
                            password: this.registerForm.password
                        })
                        .then(res => {
                            this.registering = false
                            if (res.data.code === 0) {
                                this.$message.success('注册成功')
                                this.$router.push({ path: '/login' })
                            } else {
                                this.$message.warning(res.data.msg)
                            }
                        })
                        .catch(e => {
                            this.registering = false
                            this.$message.error(e)
                        })
                } else {
                    console.log('error submit!')
                    return false
                }
            })
        },
        showTerms() {
            let html = `
                <div><p>以下类型的图片均不允许上传:</p><ul>
                <li>侵权的图片, 包括侵犯个人隐私、企业版权等;</li>
                <li>含有成人內容/擦边/偷拍/过分裸露情节的图片及成人性用品相关图片;</li>
                <li>含有恐怖、血腥以及煽动暴力、宣扬宗教、种族主义、种族仇恨等;</li>
                <li>其他非法图片(包括但不限于赌博、毒品、电脑病毒、木马、诈骗、假冒药品等非法行为);</li>
                <li>违反所在国家或地区法律法规的图片;</li>
                </ul><p>其他条款</p><ul>
                <li>即使图片不违规, 也禁止外链到非法网站或App应用程序中。</li>
                <li>用户产生的内容（即上传的图片）需自行负责，本站不承担任何法律及连带责任。</li>
                <li>管理员有权删除违规、违法、被举报等不合适的图片。</li>
                <li>不论是网页端注册还是通过接口注册，均视为您已同意服务条款和隐私政策。</li>
                <li>保留随时变更或修改服务条款部分或全部內容的权利。</li>
                </ul></div>`
            this.$alert(html, '服务条款 Terms of Service', {
                showConfirmButton: false,
                dangerouslyUseHTMLString: true,
                distinguishCancelAndClose: true
            })
        },
        showPrivacy() {
            let html = `
                <div><ul>
                <li>本站仅记录注册用户的用户名、注册时间, 这些信息仅供网站内部使用。</li>
                <li>除法律要求或用户违规外, 我们不会主动向第三方泄露您的敏感信息。</li>
                <li>由用户本人造成的账号泄露或黑客攻击、服务器故障等不可抗力造成的服务故障，本站不承担任何责任。</li>
                <li>扩展性或第三方功能造成的隐私泄露本站亦不承担任何责任。</li>
                </ul></div>`
            this.$alert(html, '隐私政策 Privacy Policy', {
                showConfirmButton: false,
                dangerouslyUseHTMLString: true,
                distinguishCancelAndClose: true
            })
        }
    }
}
</script>

<style scoped>
.register-area {
    -webkit-border-radius: 5px;
    border-radius: 5px;
    margin: 70px auto 30px;
    width: 350px;
    padding: 35px 35px 15px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
}
.register-area .agree {
    text-align: left;
    float: left;
}
</style>