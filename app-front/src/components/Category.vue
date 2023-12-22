<template>
    <section class="container">
        <a-typography-title :level="1">多媒体交互</a-typography-title>
        <p>基于数字媒体技术，我们实现了下列多种媒体类型的交互。我们希望通过这些真实的视听体验，增强公众对生态保护的认识。</p>
        <a-divider />
        <a-row :gutter="16">
            <a-col :span="8">
                <router-link to="/video">
                    <a-card hoverable class="card">
                        <div class="bg video"></div>
                        <div class="text">
                            <a-typography-title :level="4">视频交互
                                <ArrowRightOutlined class="icon" />
                            </a-typography-title>
                            <p>以视频上传为起点，提供全链路的一流视频分析能力，助力生态保护。</p>
                        </div>
                    </a-card>
                </router-link>
            </a-col>
            <a-col :span="8">
                <router-link to="/audio">
                    <a-card hoverable class="card">
                        <div class="bg audio"></div>
                        <div class="text">
                            <a-typography-title :level="4">音频交互
                                <ArrowRightOutlined class="icon" />
                            </a-typography-title>
                            <p>通过音频分析，生成语谱图、波形图等音频资料，为物种研究保驾护航。</p>
                        </div>
                    </a-card></router-link>
            </a-col>
            <a-col :span="8">
                <router-link to="/image">
                    <a-card hoverable class="card">
                        <div class="bg image"></div>
                        <div class="text">
                            <a-typography-title :level="4">图像交互
                                <ArrowRightOutlined class="icon" />
                            </a-typography-title>
                            <p>采用业界领先的图像分析技术，生成灰度直方图，实现均衡化等操作。</p>
                        </div>
                    </a-card></router-link>
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