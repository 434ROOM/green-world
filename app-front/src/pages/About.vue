<template>
    <a-layout>
        <GW-Navbar />
        <a-layout-content class="container">
            <div class="bg">
                <a-typography-title :level="1" class="title">关于我们</a-typography-title>
            </div>
            <a-card class="content">
                <section>
                    <a-typography-title :level="2">我们是谁？</a-typography-title>
                    <p>我们来自北京林业大学信息学院，是一群热爱自然、热爱生命的年轻人。</p>
                    <div class="wall">
                        <a-row :gutter="[{ xs: 8, sm: 16, md: 24, lg: 32 }, { xs: 8, sm: 16, md: 24, lg: 32 }]">
                            <a-col :span="12" :xs="24" :sm="24" :md="24" :lg="12" :xl="12">
                                <a-card hoverable class="card">
                                    <a-avatar class="avatar" size="large"
                                        src="http://q1.qlogo.cn/g?b=qq&nk=1905236008&s=640" />
                                    <a-card-meta title="申可" description="数媒22-2 后端开发" />
                                </a-card>
                            </a-col>
                            <a-col :span="12" :xs="24" :sm="24" :md="24" :lg="12" :xl="12">
                                <a-card hoverable class="card">
                                    <a-avatar class="avatar" size="large"
                                        src="http://q1.qlogo.cn/g?b=qq&nk=1533180937&s=640" />
                                    <a-card-meta title="刘子豪" description="数媒22-1 前端开发" />
                                </a-card>
                            </a-col>
                        </a-row>
                    </div>
                </section>

                <section>
                    <a-typography-title :level="2">GreenWorld 是什么？</a-typography-title>
                    <p>
                        当前，全球面临着诸多生态环境问题，如气候变化、生物多样性丧失和污染等。公众对这些问题的认识和理解对于生态环境的保护和可持续发展至关重要。
                    </p>
                    <p>
                        GreenWorld 是一个利用数字媒体中文本、图像、音频、视频相关处理技术及 Web
                        开发技术，旨在提供关于生态系统、生物多样性、环境保护等方面的知识。通过生动的视觉和听觉呈现，这个系统能够有效地传达生态环境的复杂性和对人类生活的重要性。
                    </p>
                </section>

                <section>
                    <a-typography-title :level="2">技术栈</a-typography-title>
                    <p>为了系统的美观和高效，我们使用了以下最新的技术栈。感谢开源社区为我们提供的这些优秀工具！</p>
                    <div class="wall">
                        <a-row :gutter="[{ xs: 8, sm: 16, md: 24, lg: 32 }, { xs: 8, sm: 16, md: 24, lg: 32 }]">
                            <a-col :span="8" :xs="24" :sm="24" :md="24" :lg="8" :xl="8">
                                <a href="https://www.djangoproject.com/" target="_blank">
                                    <a-card hoverable class="card">
                                        <a-avatar class="avatar" size="large" :src="djLogo" />
                                        <a-card-meta title="Django" />
                                    </a-card>
                                </a>
                            </a-col>
                            <a-col :span="8" :xs="24" :sm="24" :md="24" :lg="8" :xl="8">
                                <a href="https://vuejs.org/" target="_blank">
                                    <a-card hoverable class="card">
                                        <a-avatar class="avatar" size="large" :src="vueLogo" />
                                        <a-card-meta title="Vue.js" />
                                    </a-card>
                                </a>
                            </a-col>
                            <a-col :span="8" :xs="24" :sm="24" :md="24" :lg="8" :xl="8">
                                <a href="https://www.antdv.com/" target="_blank">
                                    <a-card hoverable class="card">
                                        <a-avatar class="avatar" size="large" :src="antdvLogo" />
                                        <a-card-meta title="Ant Design Vue" />
                                    </a-card>
                                </a>
                            </a-col>
                        </a-row>
                    </div>
                </section>

                <section>
                    <a-typography-title :level="2">项目特点</a-typography-title>
                    <a-row class="feature" :gutter="[{ xs: 8, sm: 16, md: 24, lg: 32 }, { xs: 8, sm: 16, md: 24, lg: 32 }]">
                        <a-col :span="6" :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
                            <a-card hoverable class="card">
                                <div class="img-box f1"></div>
                                <div class="text-box">
                                    <a-typography-title :level="5">
                                        <RocketFilled class="icon-mr" />前后端分离
                                    </a-typography-title>
                                    <p>API + vue 架构快速迭代，增强系统性能，为未来的可拓展模式打下基础。</p>
                                </div>
                            </a-card>
                        </a-col>
                        <a-col :span="6" :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
                            <a-card hoverable class="card">
                                <div class="img-box f2"></div>
                                <div class="text-box">
                                    <a-typography-title :level="5">
                                        <CompassFilled class="icon-mr" />交互优雅
                                    </a-typography-title>
                                    <p>使用 Ant Design Vue 组件库，提供了一套优雅的交互设计。</p>
                                </div>
                            </a-card>
                        </a-col>
                        <a-col :span="6" :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
                            <a-card hoverable class="card">
                                <div class="img-box f3"></div>
                                <div class="text-box">
                                    <a-typography-title :level="5">
                                        <BulbFilled class="icon-mr" />操作简单
                                    </a-typography-title>
                                    <p>我们尽力优化用户使用流程，降低用户使用成本。</p>
                                </div>
                            </a-card>
                        </a-col>
                        <a-col :span="6" :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
                            <a-card hoverable class="card">
                                <div class="img-box f4"></div>
                                <div class="text-box">
                                    <a-typography-title :level="5">
                                        <YuqueFilled class="icon-mr" />拥抱自然
                                    </a-typography-title>
                                    <p>以“人与自然和谐共生”为主题，助力生态保护的科普宣传。</p>
                                </div>
                            </a-card>
                        </a-col>
                    </a-row>
                </section>
            </a-card>
        </a-layout-content>
        <GW-Footer />
    </a-layout>
</template>

<script lang="ts">
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import vueLogo from '../assets/images/about/vue.png';
import antdvLogo from '../assets/images/about/antdv.png';
import djLogo from '../assets/images/about/django.png';
import {
    RocketFilled,
    CompassFilled,
    BulbFilled,
    YuqueFilled,
} from '@ant-design/icons-vue';

export default {
    components: {
        'GW-Navbar': Navbar,
        'GW-Footer': Footer,
        RocketFilled,
        CompassFilled,
        BulbFilled,
        YuqueFilled,
    },
    data() {
        return {
            vueLogo,
            antdvLogo,
            djLogo,
        };
    },
}
</script>

<style scoped>
.container {
    position: relative;
    min-height: calc(100vh - 64px - 69px);
}

.bg {
    background-image: url('../assets/images/about/stars.jpg');
    background-size: cover;
    background-position: center;
    height: 60vh;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
}

.title {
    color: white;
    margin-bottom: 3rem;
}

.content {
    position: relative;
    top: -16vh;
    width: 95%;
    margin: auto;
    padding: 1.5rem 3rem;
}

section {
    margin-bottom: 3rem;
}

section:last-child {
    margin-bottom: 0;
}

.wall {
    width: 80%;
    max-width: 800px;
    margin: 2rem auto;
}

.feature {
    width: 100%;
    margin: 2rem auto;
}

.card {
    width: 100%;
    height: 100%;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.avatar {
    margin-bottom: 1rem;
}

.img-box {
    position: absolute;
    left: 0;
    top: 0;
    z-index: 0;
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
    overflow: hidden;
}

.img-box::after {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    z-index: 1;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.8);

}

.text-box {
    position: relative;
    z-index: 2;
}

.f1 {
    background-image: url('../assets/images/about/fast.png');
}

.f2 {
    background-image: url('../assets/images/about/coperation.png');
}

.f3 {
    background-image: url('../assets/images/about/easy.png');
}

.f4 {
    background-image: url('../assets/images/about/nature.png');
}

.icon-mr {
    margin-right: 0.5rem;
}
</style>