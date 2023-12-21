<template>
    <a-layout-header class="nav-header" :class="navbarClass">
        <div class="logo">
            <RouterLink to="/">
                <img :src="logoSrc" alt="nav-logo" @mouseover="logoChange(true)" @mouseleave="logoChange(false)" />
            </RouterLink>
        </div>
        <a-menu class="menu" v-model:selectedKeys="selectedKeys" theme="light" mode="horizontal">
            <!--注意：下面的key值与router.js中的name值对应，均需首字母大写-->
            <a-menu-item key="Home"><router-link to="/">首页</router-link></a-menu-item>
            <a-menu-item key="Video"><router-link to="/video">视频交互</router-link></a-menu-item>
            <a-menu-item key="Audio"><router-link to="/audio">音频交互</router-link></a-menu-item>
            <a-menu-item key="Image"><router-link to="/image">图片交互</router-link></a-menu-item>
            <a-menu-item key="About"><router-link to="/about">关于我们</router-link></a-menu-item>
        </a-menu>
    </a-layout-header>
</template>

<script lang="ts">
import { ref } from 'vue';

import defaultSrc from '../assets/images/logo-text.png';
import hoverSrc from '../assets/images/logo-text-green.png';

const logoSrc = ref(defaultSrc);
function logoChange(ishover: boolean) {
    logoSrc.value = ishover ? hoverSrc : defaultSrc;
}

const selectedKeys = ref<string[]>(['home']);
const navbarClass = ref<string>('nav-header');

export default {
    mounted() {
        let pageName = this.$route.name;
        selectedKeys.value = [pageName];// 选中当前页面，如果name为其他默认不选中
        window.addEventListener('scroll', this.handleScroll); // 监听滚动事件
    },
    beforeUnmount() {
        window.removeEventListener('scroll', this.handleScroll); // 在组件销毁前移除监听器
    },
    methods: {
        handleScroll() {
            const scrollPosition = window.scrollY;
            // 在滚动一定距离后改变导航栏颜色
            if (scrollPosition > 64) { // 假设滚动超过64像素
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
</style>