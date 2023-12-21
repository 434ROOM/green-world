<template>
    <a-layout>
        <GW-Navbar />
        <a-layout-content>
            <GW-Banner />
            <GW-Introduction />
            <GW-OurResearch />
            <GW-Category />
            <GW-Word />
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
import Category from '../components/Category.vue';
import Word from '../components/Word.vue';

document.title = '首页 | GreenWorld - 人与自然和谐共生';

export default {
    components: {
        'GW-Navbar': Navbar,
        'GW-Footer': Footer,
        'GW-Banner': Banner,
        'GW-Introduction': Introduction,
        'GW-OurResearch': OurResearch,
        'GW-Category': Category,
        'GW-Word': Word,
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