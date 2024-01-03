<template>
    <a-layout>
        <GWNavbar />
        <a-layout-content class="bg">
            <div class="content">
                <div class="form">
                    <a-segmented v-model:value="current" block :options="switchData" size="large" />
                    <a-divider />

                    <div v-if="current == switchData[0]">
                        <a-form :model="loginFormState" name="normal_login" class="login-form" @finish="loginFinish"
                            @finishFailed="loginFinishFailed" @submit="loginRequest">
                            <a-form-item name="email" :rules="emailRules">
                                <a-input v-model:value="loginFormState.email" placeholder="邮箱">
                                    <template #prefix>
                                        <MailOutlined class="site-form-item-icon" />
                                    </template>
                                </a-input>
                            </a-form-item>

                            <a-form-item name="password" :rules="[{ required: true, message: '请输入密码！' }]">
                                <a-input-password v-model:value="loginFormState.password" placeholder="密码">
                                    <template #prefix>
                                        <LockOutlined class="site-form-item-icon" />
                                    </template>
                                </a-input-password>
                            </a-form-item>

                            <a-form-item>
                                <a-form-item name="rule" no-style>
                                    <a-checkbox v-model:checked="loginFormState.rule">
                                        我已阅读并同意
                                        <a href="https://www.rxgzs.cn/clause/">《服务条款》</a>
                                        和
                                        <a href="https://www.rxgzs.cn/privacy/">《隐私政策》</a>
                                        。
                                    </a-checkbox>
                                </a-form-item>
                            </a-form-item>

                            <a-form-item no-style>
                                <a-button :disabled="loginDisabled" type="primary" html-type="submit"
                                    class="login-form-button">
                                    登录
                                </a-button>
                            </a-form-item>
                        </a-form>
                    </div>

                    <div v-if="current == switchData[1]">
                        <a-form :model="registerFormState" name="normal_login" class="login-form" @finish="registerFinish"
                            @finishFailed="registerFinishFailed" @submit="registerRequest">
                            <a-form-item name="email" :rules="emailRules">
                                <a-input v-model:value="registerFormState.email" placeholder="邮箱">
                                    <template #prefix>
                                        <MailOutlined class="site-form-item-icon" />
                                    </template>
                                </a-input>
                            </a-form-item>

                            <a-form-item name="password" :rules="[{ required: true, message: '请输入密码！' }]">
                                <a-input-password v-model:value="registerFormState.password" placeholder="密码">
                                    <template #prefix>
                                        <LockOutlined class="site-form-item-icon" />
                                    </template>
                                </a-input-password>
                            </a-form-item>

                            <a-form-item name="confirm" :rules="[{ required: true, message: '请确认密码！' }]">
                                <a-input-password v-model:value="registerFormState.confirm" placeholder="确认密码">
                                    <template #prefix>
                                        <LockOutlined class="site-form-item-icon" />
                                    </template>
                                </a-input-password>
                            </a-form-item>

                            <a-form-item>
                                <a-form-item name="rule" no-style>
                                    <a-checkbox v-model:checked="registerFormState.rule">
                                        我已阅读并同意
                                        <a href="https://www.rxgzs.cn/clause/">《服务条款》</a>
                                        和
                                        <a href="https://www.rxgzs.cn/privacy/">《隐私政策》</a>
                                        。
                                    </a-checkbox>
                                </a-form-item>
                            </a-form-item>

                            <a-form-item no-style>
                                <a-button :disabled="registerDisabled" type="primary" html-type="submit"
                                    class="login-form-button">
                                    注册
                                </a-button>
                            </a-form-item>
                        </a-form>
                    </div>


                </div>
            </div>
        </a-layout-content>
        <GWFooter />
    </a-layout>
</template>

<script setup lang="ts">
import GWNavbar from '@/components/Navbar.vue';
import GWFooter from '@/components/Footer.vue';
import { reactive, computed } from 'vue';
import { MailOutlined, LockOutlined } from '@ant-design/icons-vue';
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { message } from 'ant-design-vue';

// 获取当前路由的查询参数对象
const route = useRoute();
const queryParams = route.query;
const redirect = queryParams.redirect as string;

// 正则表达式验证邮箱格式
function validateEmail(email: string) {
    let reg = /^([a-zA-Z]|[0-9])(\w|-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
    return reg.test(email);
}
const emailRules = [
    {
        required: true,
        message: '请输入邮箱！',
    },
    {
        validator: (rule: any, value: string) => {
            if (value && !validateEmail(value)) {
                return Promise.reject('邮箱格式不正确！');
            } else {
                return Promise.resolve();
            }
        },
    },
];

// 切换登录注册
const switchData = reactive(['登录', '注册']);
const current = ref(switchData[0]);

// 登录表单
interface LoginFormState {
    email: string;
    password: string;
    rule: boolean;
}
const loginFormState = reactive<LoginFormState>({
    email: '',
    password: '',
    rule: true,
});
const loginFinish = (values: any) => {
    console.log('Success:', values);
};

const loginFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
};
const loginDisabled = computed(() => {
    return !(loginFormState.email && loginFormState.password && loginFormState.rule);
});
function loginRequest(){

}

// 注册表单
interface RegisterFormState {
    email: string;
    password: string;
    confirm: string;
    rule: boolean;
}

const registerFormState = reactive<RegisterFormState>({
    email: '',
    password: '',
    confirm: '',
    rule: true,
});

const registerFinish = (values: any) => {
    console.log('Success:', values);
};

const registerFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
};

const registerDisabled = computed(() => {
    let isFinish = registerFormState.email && registerFormState.password && registerFormState.confirm && registerFormState.rule;
    let isSame = registerFormState.password === registerFormState.confirm;
    return !(isFinish && isSame);
});
function registerRequest(){

}

</script>

<style scoped>
.bg {
    width: 100%;
    height: 100vh;
    padding-top: 64px;
    background-color: #fff;
    background-image: url(../assets/images/login/login-bg.jpg);
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
}

.content {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 1rem;
}

.form {
    width: 100%;
    max-width: 400px;
    padding: 2.5rem 3rem;
    background-color: #fff;
    border-radius: .5rem;
    box-shadow: 0 0 10px rgba(0, 0, 0, .1);
}

.form a {
    color: #00b96b;
}

.form a:hover {
    color: #00a65b96;
}

.login-form {
    width: 100%;
}

.login-form-forgot {
    text-align: center;
    margin-top: 1rem;
    margin-bottom: 0;
}

.login-form-button {
    width: 100%;
}
</style>