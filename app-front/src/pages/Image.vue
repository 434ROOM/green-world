<template>
    <a-layout>
        <GW-Navbar />
        <a-layout class="container">
            <GW-Sider />
            <a-layout class="right">
                <a-layout-content class="content">
                    <a-typography-title :level="1">图像交互</a-typography-title>
                    <a-divider />
                    <ImageSteps />
                </a-layout-content>
                <GW-Footer />
            </a-layout>
        </a-layout>
    </a-layout>
</template>


<script lang="ts">

import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import Sider from '../components/Sider.vue';
import ImageSteps from '@/components/ImageSteps.vue';

export default {
    components: {
        'GW-Navbar': Navbar,
        'GW-Footer': Footer,
        'GW-Sider': Sider,
        'ImageSteps': ImageSteps,
    },
}
</script>


<style scoped>
.container {
    width: 100%;
    height: calc(100vh - 64px);
    margin-top: 64px;
    padding: 0;
}
.right{
    width: 100%;
    height: 100%;
    overflow:auto;
}
.content {
    width: 100%;
    min-height: calc(100vh - 64px);
    background-color: #fff;
    padding: 2rem 3rem;
}
</style>
  