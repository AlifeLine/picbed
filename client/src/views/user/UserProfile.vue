<template>
    <div class="user-profile">
        <el-tabs tab-position="left">
            <el-tab-pane label="个人资料">
                <el-row>
                    <el-col :span="12">
                        <el-form
                            ref="userProfile"
                            :model="userProfile"
                            :rules="profileRules"
                            label-width="100px"
                        >
                            <el-row :gutter="5">
                                <el-col :span="24">
                                    <el-form-item label="昵称" prop="nickname">
                                        <el-input
                                            v-model="userProfile.nickname"
                                            placeholder="请输入昵称"
                                            clearable
                                            :style="{width: '100%'}"
                                        ></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="24">
                                    <el-form-item label="邮箱" prop="email">
                                        <el-input
                                            v-model="userProfile.email"
                                            placeholder="请输入邮箱"
                                            clearable
                                            :style="{width: '100%'}"
                                        ></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="18">
                                    <el-form-item label="头像" prop="avatar">
                                        <el-input
                                            v-model="userProfile.avatar"
                                            placeholder="请输入头像URL地址"
                                            clearable
                                            :style="{width: '100%'}"
                                        ></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="6">
                                    <el-form-item label-width="0" prop="upload">
                                        <el-button
                                            type="primary"
                                            icon="el-icon-upload"
                                            size="mini"
                                        >上传头像</el-button>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="24">
                                    <el-form-item size="small">
                                        <el-button type="primary" @click="submitProfileForm">保存资料</el-button>
                                        <el-button @click="resetProfileForm">重置</el-button>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-col>
                </el-row>
            </el-tab-pane>
            <el-tab-pane label="账号安全">
                <el-row>
                    <el-col :span="12">
                        <el-form
                            ref="userPasswd"
                            :model="userPasswd"
                            :rules="passwdRules"
                            label-width="100px"
                        >
                            <el-form-item label="新密码" prop="new_passwd">
                                <el-input
                                    v-model="userPasswd.new_passwd"
                                    placeholder="请输入新密码"
                                    clearable
                                    show-password
                                ></el-input>
                            </el-form-item>
                            <el-form-item label="当前密码" prop="old_passwd">
                                <el-input
                                    v-model="userPasswd.old_passwd"
                                    placeholder="请输入当前密码"
                                    clearable
                                    show-password
                                ></el-input>
                            </el-form-item>
                            <el-form-item size="small">
                                <el-button type="primary" @click="submitPasswdForm">修改密码</el-button>
                                <el-button @click="resetPasswdForm">重置</el-button>
                            </el-form-item>
                        </el-form>
                    </el-col>
                </el-row>
            </el-tab-pane>
            <el-tab-pane label="Api">
                <el-link type="danger">初始化生成密钥</el-link>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>
<script>
import { mutations, state } from '@/libs/store.js'
export default {
    name: 'UserProfile',
    data() {
        return {
            userProfile: {
                nickname: this.$store.state.nickname,
                email: this.$store.state.email,
                avatar: this.$store.state.avatar,
                token: this.$store.state.token
            },
            profileRules: {
                email: [
                    {
                        required: true,
                        message: '请输入邮箱',
                        trigger: 'blur'
                    },
                    {
                        type: 'email',
                        message: '请输入正确的邮箱地址',
                        trigger: 'change'
                    }
                ],
                avatar: [
                    {
                        type: 'url',
                        message: `请输入正确的URL`,
                        trigger: 'change'
                    }
                ]
            },
            userPasswd: {
                new_passwd: undefined,
                old_passwd: undefined
            },
            passwdRules: {
                new_passwd: [
                    {
                        required: true,
                        message: '请输入新密码',
                        trigger: 'blur'
                    },
                    {
                        pattern: /^[\S]{6,32}$/,
                        message: '密码要求6-32位且无空格',
                        trigger: 'blur'
                    }
                ],
                old_passwd: [
                    {
                        required: true,
                        message: '请输入当前密码',
                        trigger: 'blur'
                    }
                ]
            }
        }
    },
    methods: {
        submitProfileForm() {
            this.$refs['userProfile'].validate((valid) => {
                if (!valid) return
                // TODO 提交表单
            })
        },
        resetProfileForm() {
            this.$refs['userProfile'].resetFields()
        },
        submitPasswdForm() {
            this.$refs['userPasswd'].validate((valid) => {
                if (!valid) return
                // TODO 提交表单
            })
        },
        resetPasswdForm() {
            this.$refs['userPasswd'].resetFields()
        }
    }
}
</script>
