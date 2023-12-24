<template>
    <a-layout>
        <GW-Navbar />
        <a-layout-content class="content">
            <div class="center">
                <a-result status="404" title="404 Not Found" sub-title="抱歉，您访问的页面走丢了。">
                    <template #extra>
                        <a-button type="primary">回到首页</a-button>
                    </template>
                </a-result>
            </div>
        </a-layout-content>
        <GW-Footer />
    </a-layout>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';

export default {
    name: 'NotFound',
    components: {
        'GW-Navbar': Navbar,
        'GW-Footer': Footer
    }
}
</script>

<style scoped>
.content {
    min-height: 100vh;
    background-color: #fff;
}

.center {
    width: 100%;
    height: calc(100vh - 64px);
    margin-top: 64px;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>