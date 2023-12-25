<template>
    <a-layout-footer>
        <a-divider />
        <a-row class="footer" :gutter="[{ xs: 8, sm: 16, md: 24, lg: 32 }, { xs: 8, sm: 16, md: 24, lg: 32 }]">
            <a-col class="gutter-row" :span="6" :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
                <div class="gutter-box logo-area">
                    <RouterLink to="/">
                        <img class="logo" :src="logoSrc" alt="nav-logo" @mouseover="logoChange(true)"
                            @mouseleave="logoChange(false)" />
                    </RouterLink>
                    <h3 class="slogan">人与自然和谐共生</h3>
                </div>
            </a-col>
            <a-col class="gutter-row link-area" :span="6" :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
                <div class="gutter-box">
                    <a-typography-title :level="4">站点</a-typography-title>
                    <a-typography-paragraph>
                        <RouterLink to="/">首页</RouterLink>
                    </a-typography-paragraph>
                    <a-typography-paragraph>
                        <RouterLink to="/about">关于我们</RouterLink>
                    </a-typography-paragraph>
                </div>
            </a-col>
            <a-col class="gutter-row link-area" :span="6" :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
                <div class="gutter-box">
                    <a-typography-title :level="4">链接</a-typography-title>
                    <a-typography-paragraph>
                        <a href="https://www.unep.org/" target="_blank">联合国环境规划署 - UNEP</a>
                    </a-typography-paragraph>
                    <a-typography-paragraph>
                        <a href="https://www.bjfu.edu.cn" target="_blank">北京林业大学</a>
                    </a-typography-paragraph>
                </div>
            </a-col>
            <a-col class="gutter-row link-area" :span="6" :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
                <div class="gutter-box">
                    <a-typography-title :level="4">联系我们</a-typography-title>
                    <a-typography-paragraph>
                        <a href="mailto:ChrisLiu@bjfu.edu.cn">Email</a>
                    </a-typography-paragraph>
                </div>
            </a-col>
        </a-row>
        <a-typography-paragraph class="link-area copyright">
            <a href="//rxgzs.cn/clause" target="_blank">服务条款</a>
            <a-divider type="vertical" />
            <a href="//rxgzs.cn/privacy" target="_blank">隐私政策</a>
            <a-divider type="vertical" />
            <a href="https://beian.miit.gov.cn/" target="_blank">京ICP备2023017692号-1</a>
            <br>
            Built with <a href="https://www.djangoproject.com/" target="_blank">Django</a> and <a href="https://vuejs.org/"
                target="_blank">Vue</a>. Colored with <a href="https://antdv.com" target="_blank">Ant Design Vue</a>.
            <br>
            Copyright © 2023 GreenWorld Team All rights reserved.
        </a-typography-paragraph>
    </a-layout-footer>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import defaultSrc from '../assets/images/logo-text.png';
import hoverSrc from '../assets/images/logo-text-green.png';
const logoSrc = ref(defaultSrc);
function logoChange(ishover: boolean) {
    logoSrc.value = ishover ? hoverSrc : defaultSrc;
}
</script>

<style scoped>
.footer {
    padding: 24px 0;

}

.logo-area {
    text-align: center;
}

.logo-area .logo {
    width: 80%;
    height: auto;
}

.slogan {
    font-size: 1rem;
    font-weight: 400;
}

.link-area a {
    color: black;
}

.link-area a:hover {
    color: #00b96b;
}

.copyright {
    text-align: center;
}
</style>