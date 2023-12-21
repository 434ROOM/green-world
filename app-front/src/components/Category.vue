<template>
    <section class="container">
        <a-typography-title :level="1">多媒体交互</a-typography-title>
        <p>基于数字媒体技术，我们实现了下列多种媒体类型的交互。我们希望通过这些真实的视听体验，增强公众对生态保护的认识。</p>
        <a-divider />
        <a-row :gutter="16">
            <a-col :span="8">
                <a-card hoverable class="card">
                    <div class="bg video"></div>
                    <div class="text">
                        <a-typography-title :level="4">视频交互<ArrowRightOutlined class="icon" /></a-typography-title>
                        <p>我们通过视频的形式，展示了生态保护的现状，以及我们的项目成果。</p>
                    </div>
                </a-card>
            </a-col>
            <a-col :span="8">
                <a-card hoverable  class="card">
                    <div class="bg audio"></div>
                    <div class="text">
                        <a-typography-title :level="4">音频交互<ArrowRightOutlined class="icon" /></a-typography-title>
                        <p>我们通过音频的形式，让公众了解生态保护的现状，以及我们的项目成果。</p>
                    </div>
                </a-card>
            </a-col>
            <a-col :span="8">
                <a-card hoverable  class="card">
                    <div class="bg image"></div>
                    <div class="text">
                        <a-typography-title :level="4">图片交互<ArrowRightOutlined class="icon" /></a-typography-title>
                        <p>我们通过图片的形式，让公众了解生态保护的现状，以及我们的项目成果。</p>
                    </div>
                </a-card>
            </a-col>
        </a-row>
    </section>
</template>

<script lang="ts" setup>
import { ArrowRightOutlined } from '@ant-design/icons-vue';
</script>

<style scoped>
.container {
    width: 100%;
    height: auto;
    margin: auto;
    padding: 8rem 16%;
}

.card {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
    transition: all .3s;
}

.card:hover {
    transform: scale(1.01);
}

.icon {
    margin-left: .5rem;
    transition: all .3s;
}

.card:hover .icon {
    transform: translateX(10px);
}

.bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}


.bg::after {
    width: 100%;
    height: 100%;
    content: '';
    position: absolute;
    z-index: 1;
    top: 0;
    left: 0;
    background-image: linear-gradient(90deg, #ffffff 10%, #ffffff61 100%);
}

.video {
    background: url('../assets/images/index/video.png');
    background-size: 80%;
    background-repeat: no-repeat;
    background-position: right -80% bottom 50%;
}

.audio {
    background: url('../assets/images/index/audio.png');
    background-size: 80%;
    background-repeat: no-repeat;
    background-position: right -80% bottom 50%;
}

.image {
    background: url('../assets/images/index/image.png');
    background-size: 80%;
    background-repeat: no-repeat;
    background-position: right -80% bottom 50%;
}

.text {
    position: relative;
    z-index: 2;
    padding-right: 20%;
}
</style>