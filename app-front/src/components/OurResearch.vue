<template>
    <div class="bg">
        <a-typography-title :level="1" class="title">
            <ExperimentOutlined class="icon-mr" />我们的研究
        </a-typography-title>
        <div class="cards">
            <a-card hoverable class="voice-card left">
                <template #cover>
                    <img alt="example" src="../assets/images/index/sound.jpg" />
                </template>
                <a-card-meta title="鸟类叫声">
                </a-card-meta>
                <p>我们通过数字媒体技术，对鸟类叫声的音频进行处理，生成相应的语谱图。这有助于对鸟类的种群研究，保护生态多样性。</p>
                <audio loop ref="audioPlayer">
                    <source :src="BirdsSound" />
                </audio>
                <a-button type="primary" :icon="h(isPlaying ? PauseCircleFilled : PlayCircleFilled)"
                    @click="playPauseAudio">
                    {{ isPlaying ? '暂停声音' : '播放声音' }}
                </a-button>
            </a-card>
            <a-card hoverable class="voice-card right">
                <template #cover>
                    <img alt="example" src="../assets/images/index/ypt.png" />
                </template>
                <a-card-meta title="鸟类叫声的语谱图">

                </a-card-meta>
                <p>这是我们通过数字媒体技术，对上述鸟类叫声处理后生成的语谱图。</p>
                <a-button type="primary" :icon="h(SearchOutlined)" @click="showModal">查看更多</a-button>
                <a-modal v-model:open="open" title="查看更多" @ok="handleOk" :footer="null">
                    <a-image :src="yptTextImage" alt="" class="big-img"></a-image>
                </a-modal>
            </a-card>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { h } from 'vue';
import { ref } from 'vue';
import {
    ExperimentOutlined,
    PlayCircleFilled,
    PauseCircleFilled,
    SearchOutlined,
} from '@ant-design/icons-vue';
import BirdsSound from '@/assets/birds-sound.mp3';
import yptTextImage from '@/assets/images/index/ypt-text.png';

const audioPlayer = ref<HTMLAudioElement | null>(null);
const isPlaying = ref(false);

function playPauseAudio() {
    if (isPlaying.value === false) {
        audioPlayer.value.play(); // 播放音频
        //console.log('play');
        isPlaying.value = true;
    }
    else {
        audioPlayer.value.pause(); // 暂停音频
        //console.log('pause');
        isPlaying.value = false;
    }
}

const open = ref<boolean>(false);

const showModal = () => {
  open.value = true;
};

const handleOk = (e: MouseEvent) => {
  console.log(e);
  open.value = false;
};
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
    transition: all 0.5s ease;
}

.left {
    position: relative;
    z-index: 1;
    left: -30%;
}

.left:hover {
    z-index: 3;
}

.right {
    position: relative;
    z-index: 2;
    right: -30%;
    top: -30%;
}

.big-img{
    width: 100%;
    height: auto;
}
</style>