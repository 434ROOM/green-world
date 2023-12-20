<template>
    <a-layout>
        <GW-Navbar />
        <a-layout-content>
            <GW-Banner />
            <GW-Introduction />
            <GW-OurResearch />
            <div :style="{ background: '#fff', padding: '24px', minHeight: '1000px' }">
                Content
                <br>
                88888888888
                <br>
                88888888888
                <br>
                88888888888
            </div>
        </a-layout-content>
        <GW-Footer />
    </a-layout>
</template>

<script lang="ts">
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import Banner from '../components/Banner.vue';
import Introduction from '../components/Introduction.vue';
import OurResearch from '../components/OurResearch.vue';

document.title = '首页 | GreenWorld - 人与自然和谐共生';

export default {
    components: {
        'GW-Navbar': Navbar,
        'GW-Footer': Footer,
        'GW-Banner': Banner,
        'GW-Introduction': Introduction,
        'GW-OurResearch': OurResearch,
    },
}
</script>

<style scoped>
.content {
    margin-top: 64px;
    padding: 0;
}

.site-layout .site-layout-background {
    background: #fff;
}
</style>