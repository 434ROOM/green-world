<template>
    <a-layout-header class="nav-header" :class="navbarClass">
        <div class="logo">
            <RouterLink to="/">
                <img :src="logoSrc" alt="nav-logo" @mouseover="logoChange(true)" @mouseleave="logoChange(false)" />
            </RouterLink>
        </div>
        <div class="login">
            <a-button v-if="!isLogin" type="primary" shape="round" ghost>
                <RouterLink to="/login">登录/注册</RouterLink>
            </a-button>

            <a-dropdown v-if="isLogin">
                <a class="ant-dropdown-link" @click.prevent>
                    <a-avatar :src="avatar">{{ avatarText }}</a-avatar>
                </a>
                <template #overlay>
                    <a-menu>
                        <a-menu-item>
                            <RouterLink to="/user">{{ username }}</RouterLink>
                        </a-menu-item>
                        <a-menu-item>
                            <a @click="handleLogout">
                                <LogoutOutlined /> 注销
                            </a>
                        </a-menu-item>
                    </a-menu>
                </template>
            </a-dropdown>
        </div>
        <a-menu class="menu" v-model:selectedKeys="selectedKeys" theme="light" mode="horizontal">
            <!--注意：下面的key值与router.js中的name值对应，均需首字母大写-->
            <a-menu-item key="Home"><router-link to="/">首页</router-link></a-menu-item>
            <a-menu-item key="Video"><router-link to="/video">视频交互</router-link></a-menu-item>
            <a-menu-item key="Audio"><router-link to="/audio">音频交互</router-link></a-menu-item>
            <a-menu-item key="Image"><router-link to="/image">图像交互</router-link></a-menu-item>
            <a-menu-item key="About"><router-link to="/about">关于我们</router-link></a-menu-item>
        </a-menu>
    </a-layout-header>
</template>

<script lang="ts">
import { ref } from 'vue';
import { LogoutOutlined } from '@ant-design/icons-vue';

import JWTToken from '@/JWTToken';
import EventBus from '@/EventBus';

import defaultSrc from '../assets/images/logo-text.png';
import hoverSrc from '../assets/images/logo-text-green.png';

const logoSrc = ref(defaultSrc);
function logoChange(ishover: boolean) {
    logoSrc.value = ishover ? hoverSrc : defaultSrc;
}

const selectedKeys = ref<string[]>(['home']);
const navbarClass = ref<string>('nav-header');

const isLogin = ref<boolean>(false);
const avatarText = ref<string>('');
const avatar = ref<string>('');
const username = ref<string>('');

function getLoginInfo() {
    if (JWTToken.hasToken()) {
        isLogin.value = true;
        username.value = JWTToken.getUsername();
        avatarText.value = username.value[0].toUpperCase();
        avatar.value = JWTToken.getAvatar();
    } else {
        isLogin.value = false;
        return;
    }
}

function handleLogout() {
    JWTToken.logout();
    isLogin.value = false;
}

export default {
    components: {
        LogoutOutlined,
    },
    mounted() {
        // 获取当前页面的路由名称
        let pageName = this.$route.name;
        selectedKeys.value = [pageName];
        // 监听滚动事件
        window.addEventListener('scroll', this.handleScroll);
        // 获取登录信息
        getLoginInfo();
        EventBus.on('userProfileChanged', getLoginInfo);
    },
    beforeUnmount() {
        window.removeEventListener('scroll', this.handleScroll); // 在组件销毁前移除监听器
    },
    methods: {
        handleScroll() {
            const scrollPosition = window.scrollY;
            // 在滚动一定距离后改变导航栏颜色
            if (scrollPosition > 64) { // 滚动超过64像素
                navbarClass.value = 'nav-header scrolled'
            } else {
                navbarClass.value = 'nav-header'; // 恢复导航栏颜色
            }
        },
    },
    data() {
        return {
            logoSrc,
            logoChange,
            selectedKeys,
            navbarClass,
            isLogin,
            JWTToken,
            avatar,
            username,
            handleLogout,
            avatarText,
        };
    },
}

</script>

<style scoped>
.nav-header {
    position: fixed;
    z-index: 100;
    width: 100%;
    background: transparent;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}

.scrolled {
    background: #ffffff85;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.nav-header .menu {
    line-height: 64px;
    background: rgba(255, 255, 255, 0);
}

.nav-header .logo {
    width: 120px;
    height: auto;
    background: transparent;
    margin: 0 24px 0 0;
    float: left;
}

.nav-header .logo img {
    width: 100%;
    transition: transform 0.3s ease
}

.login {
    float: right;
    margin: 0;
}
</style>