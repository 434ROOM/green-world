<template>
    <a-steps :current="current" :items="items"></a-steps>
    <div class="steps-content">
        <div v-if="current == 0">
            <a-row class="row" :gutter="32">
                <a-col :span="12">
                    <a-card hoverable class="card">
                        <img src="../assets/images/interacteion/icon-upload.png" alt="">
                        <div class="text-area">
                            <a-typography-title :level="5" class="title"> 还没有视频？</a-typography-title>
                            <p>请前往视频库上传一个，然后开始吧！</p>
                            <a-button type="primary" class="btn">
                                <router-link to="/video/lib">去上传</router-link>
                            </a-button>
                        </div>
                    </a-card>
                </a-col>
                <a-col :span="12">
                    <a-card hoverable class="card">
                        <img src="../assets/images/interacteion/icon-select.png" alt="">
                        <div class="text-area">
                            <a-typography-title :level="5" class="title">已有视频？</a-typography-title>
                            <p>从您已上传的视频库中选择一个视频。</p>
                            <a-button type="primary" class="btn" @click="openVideoSelector">选一个</a-button>

                            <a-modal v-model:open="open" title="选择视频" @ok="selectVideo">
                                <template #footer>
                                    <a-button key="back" @click="closeSelector">取消</a-button>
                                    <a-button key="submit" type="primary" @click="selectVideo" :disabled="!isSelect">
                                        确定
                                    </a-button>
                                </template>

                                <a-select class="selector" :loading="isLoadding" @change="handleChange"
                                    placeholder="请选择一个视频" optionLabelProp="name">
                                    <a-select-option v-for="video in videoList" :value="video.uid" :name="video.name">
                                        <img class="selector-video" :src="video.cover" :alt="video.name" />
                                        <span style="margin-left: 10px">{{ video.name }}</span>
                                    </a-select-option>
                                </a-select>

                            </a-modal>

                        </div>
                    </a-card>
                </a-col>
            </a-row>
        </div>

        <div v-if="current == 1">
            <div class="waiting">
                <a-spin :indicator="indicator" />
                <p style="margin-top: 2rem;">视频处理中，请稍后...</p>
            </div>
        </div>

        <div v-if="current == 2">
            <a-result status="success" title="视频分析成功！" sub-title="请在下方查看结果，或重新开始选择另一个视频。">
                <template #extra>
                    <a-button type="primary" @click="restart">重新开始</a-button>
                </template>
            </a-result>

            <a-descriptions :title="videoInfo.title + ' 处理结果'" bordered
                :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 2, xs: 1 }">
                <a-descriptions-item label="文件名">{{ videoInfo.title }}</a-descriptions-item>
                <a-descriptions-item label="文件 id">{{ videoInfo.id }}</a-descriptions-item>
                <a-descriptions-item label="视频时长">{{ videoInfo.duration }}</a-descriptions-item>
                <a-descriptions-item label="帧率">{{ videoInfo.fps }}</a-descriptions-item>
                <a-descriptions-item label="总帧数">{{ videoInfo.frames }}</a-descriptions-item>
                <a-descriptions-item label="视频宽度">{{ videoInfo.width }}</a-descriptions-item>
                <a-descriptions-item label="视频高度">{{ videoInfo.height }}</a-descriptions-item>
                <a-descriptions-item label="视频封面">
                    <a-image width="200px" :src="videoInfo.cover"></a-image>
                </a-descriptions-item>
                <a-descriptions-item label="视频文件">
                    <a-button type="primary" @click="videoPreview">查看视频</a-button>
                    <a-modal :open="isOpenVideo" :title="videoInfo.title" :footer="null"
                        @cancel="closeVideoReview">
                        <video width="100%" controls style="margin-top: 1rem;">
                            <source :src="videoInfo.video_file">
                            您的浏览器不支持 HTML5 video 标签。
                        </video>
                    </a-modal>
                </a-descriptions-item>
            </a-descriptions>
        </div>

    </div>
</template>


<script setup>
import { ref } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';
import Server from '../serverConfig.js';
import { LoadingOutlined } from '@ant-design/icons-vue';
import { h } from 'vue';
const indicator = h(LoadingOutlined, {
    style: {
        fontSize: '4rem',
    },
    spin: true,
});

const selectedId = ref(0);
const isLoadding = ref(false);
const open = ref(false);
const isSelect = ref(false);

function openVideoSelector() {
    getVideoList();
    isSelect.value = false;
    open.value = true;
}

function closeSelector() {
    open.value = false;
    isSelect.value = false;
}

function handleChange(value) {
    selectedId.value = value;
    isSelect.value = true;
    //console.log(selectedId.value);
}

function selectVideo() {
    open.value = false;
    stepNext();
    setTimeout(() => {
        requestVideoInfo(selectedId.value);
    }, 3000);
}

const videoInfo = ref({});
function requestVideoInfo(id) {
    axios({
        method: 'get',
        url: Server.apiUrl + '/video?id=' + id,
        accept: 'application/json',
    })
        .then((res) => {
            if (res.data.code === 200) {
                message.success("请求成功！");
                const newVideoInfo = {
                    id: res.data.data[0].id,
                    title: res.data.data[0].title,
                    video_file: Server.url + res.data.data[0].video_file,
                    duration: res.data.data[0].duration,
                    fps: res.data.data[0].fps,
                    frames: res.data.data[0].frames,
                    width: res.data.data[0].width,
                    height: res.data.data[0].height,
                    cover: Server.url + res.data.data[0].cover,
                };
                videoInfo.value = newVideoInfo;
                stepNext();
            } else {
                throw new Error(res.data.code + " " + res.data.msg); // 抛出一个错误，进入到 catch 中
            }
        })
        .catch((error) => {
            console.error(error.message); // 错误处理
            message.error("请求失败，请刷新页面稍后重试！", 0); // 错误提示
            //等待3秒后刷新页面
            setTimeout(() => {
                window.location.reload();
            }, 3000);
            return false; // 返回 false 表示请求失败
        });
}

const videoList = ref([]);
function getVideoList() {
    const getLoading = message.loading('视频列表加载中...', 0);
    isLoadding.value = true;
    axios({
        method: 'get',
        url: Server.apiUrl + '/video',
        accept: 'application/json',
    })
        .then((res) => {
            if (res.status === 200) {
                let newlist = [];
                for (let i = 0; i < res.data.data.length; i++) {
                    newlist.push({
                        uid: res.data.data[i].id,
                        name: res.data.data[i].title,
                        cover: Server.url + res.data.data[i].cover,
                    });
                }
                videoList.value = newlist;
                getLoading(); // 关闭 loading message
                isLoadding.value = false;
                message.success("视频列表加载完成！");
            } else if (res.status === 204) {
                videoList.value = [];
                getLoading(); // 关闭 loading message
                isLoadding.value = false;
                message.warning("视频列表为空，请先上传！");
            } else {
                throw new Error(res.data.code + " " + res.data.msg); // 抛出一个错误，进入到 catch 中
            }
        })
        .catch((error) => {
            console.error(error.message); // 错误处理
            isLoadding.value = false;
            getLoading(); // 关闭 loading message
            message.error("请求失败，请稍后重试！"); // 错误提示
            return false; // 返回 false 表示请求失败
        });
}


function restart() {
    current.value = 0;
}

const current = ref(0);
const stepNext = () => {
    current.value++;
};
const stepPrev = () => {
    current.value--;
};

const steps = [
    {
        title: '选择视频',
    },
    {
        title: '处理视频',
    },
    {
        title: '输出结果',
    },
];
const items = steps.map(item => ({ key: item.title, title: item.title }));

// 视频预览
const isOpenVideo = ref(false);
function videoPreview() {
    isOpenVideo.value = true;
}

function closeVideoReview() {
    isOpenVideo.value = false;
}
</script>


<style scoped>
.steps-content {
    width: 100%;
    height: fit-content;
    min-height: 60vh;
    margin-top: 1.5rem;
    border: 1px dashed #e9e9e9;
    border-radius: .5rem;
    background-color: #fafafa;
    text-align: center;
    padding: 30px 50px;
    display: grid;
    align-items: center;
}

.row {
    width: 100%;
    margin: 0 auto;
    padding: 0 10%;
    text-align: left;
}

.card {
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.card img {
    position: absolute;
    z-index: 1;
    width: 16rem;
    height: auto;
    bottom: -42%;
    right: 0;
}

.text-area {
    position: relative;
    z-index: 2;
}

.title {
    margin-bottom: 1rem;
}

.btn {
    margin-top: 1.5rem;
}

.selector {
    width: 60%;
    margin: 2rem auto;
}

.selector-video {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 0.3rem;
}

.waiting {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}


[data-theme='dark'] .steps-content {
    background-color: #2f2f2f;
    border: 1px dashed #404040;
}
</style>
  