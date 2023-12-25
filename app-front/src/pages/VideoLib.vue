<template>
    <a-layout has-sider>
        <GW-Navbar />
        <a-layout class="container">
            <GW-Sider @isSmallScreen="handleSmallScreen" />
            <a-layout class="right" :style="rightStyle">
                <a-layout-content class="content">
                    <a-typography-title :level="1">视频库</a-typography-title>
                    <a-divider />
                    <VideoUpload />
                </a-layout-content>
                <GW-Footer />
            </a-layout>
        </a-layout>
    </a-layout>
</template>


<script lang="ts">
import { ref } from 'vue';
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import Sider from '../components/Sider.vue';
import VideoUpload from '../components/VideoUpload.vue';

const rightStyle = ref({
    marginLeft: '200px'
});

export default {
    components: {
        'GW-Navbar': Navbar,
        'GW-Footer': Footer,
        'GW-Sider': Sider,
        'VideoUpload': VideoUpload,
    },
    methods: {
        handleSmallScreen(isSmallScreen: boolean) {
            if (isSmallScreen) {
                rightStyle.value.marginLeft = '0';
            } else {
                rightStyle.value.marginLeft = '200px';
            }
        }
    },
    setup() {
        return {
            rightStyle,
        }
    }
}
</script>


<style scoped>
.container {
    width: 100%;
    height: calc(100vh - 64px);
    margin-top: 64px;
    padding: 0;
}

.right {
    width: 100%;
    height: 100%;
    overflow: auto;
    margin-left: 200px;
}

.content {
    width: 100%;
    min-height: calc(100vh - 64px);
    background-color: #fff;
    padding: 2rem 3rem;
}
</style>
  