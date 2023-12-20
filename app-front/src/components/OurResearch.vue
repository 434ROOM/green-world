<template>
    <div class="bg">
        <a-typography-title :level="1" class="title">
            <ExperimentOutlined class="icon-mr" />我们的研究
        </a-typography-title>
        <div class="cards">
            <a-card class="voice-card left">
                <template #cover>
                    <img alt="example" src="../assets/images/index/sound.jpg" />
                </template>
                <a-card-meta title="鸟类叫声">

                </a-card-meta>
                <p>我们通过数字媒体技术，对鸟类叫声的音频进行处理，生成相应的语谱图。这有助于对鸟类的种群研究，保护生态多样性。</p>
                <a-button type="primary" class="card-btn">播放声音</a-button>
            </a-card>
            <a-card class="voice-card right">
                <template #cover>
                    <img alt="example" src="../assets/images/index/sound.jpg" />
                </template>
                <a-card-meta title="鸟类叫声的语谱图">

                </a-card-meta>
                <p>这是我们通过数字媒体技术，对上述鸟类叫声处理后生成的语谱图。</p>
            </a-card>
        </div>
    </div>
</template>

<script lang="ts" setup>
import {
    ExperimentOutlined,
} from '@ant-design/icons-vue';
</script>

<style scoped>
.icon-mr {
    margin-right: 0.8rem;
}

.bg {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
    height: 1000px;
    background-image: url(../assets/images/index/trees.jpg);
}

.title {
    color: white;
    margin-bottom: 3rem;
}

.cards {
    position: relative;
    height: 650px;
}

.voice-card {
    width: 600px;
    height: auto;
}

.card-btn {
    margin-bottom: 1rem;
}

.left {
    position: relative;
    z-index: 1;
    left: -30%;
}

.right {
    position: relative;
    z-index: 2;
    right: -30%;
    top: -30%;
}</style>