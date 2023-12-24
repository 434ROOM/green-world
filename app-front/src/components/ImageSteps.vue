<template>
    <a-steps :current="current" :items="items"></a-steps>
    <div class="steps-content">
        <div v-if="current == 0">
            <a-row class="row" :gutter="32">
                <a-col :span="12">
                    <a-card hoverable class="card">
                        <img src="../assets/images/interacteion/icon-upload.png" alt="">
                        <div class="text-area">
                            <a-typography-title :level="5" class="title"> 还没有图像？</a-typography-title>
                            <p>请前往图像库上传一张，然后开始吧！</p>
                            <a-button type="primary" class="btn">
                                <router-link to="/image/lib">去上传</router-link>
                            </a-button>
                        </div>
                    </a-card>
                </a-col>
                <a-col :span="12">
                    <a-card hoverable class="card">
                        <img src="../assets/images/interacteion/icon-select.png" alt="">
                        <div class="text-area">
                            <a-typography-title :level="5" class="title">已有图像？</a-typography-title>
                            <p>从您已上传的图像库中选择一张图像。</p>
                            <a-button type="primary" class="btn" @click="openImageSelector">选一张</a-button>

                            <a-modal v-model:open="open" title="选择图像" @ok="selectImage">
                                <template #footer>
                                    <a-button key="back" @click="closeSelector">取消</a-button>
                                    <a-button key="submit" type="primary" @click="selectImage" :disabled="!isSelect">
                                        确定
                                    </a-button>
                                </template>

                                <a-select class="selector" :loading="isLoadding" @change="handleChange"
                                    placeholder="请选择一张图像" optionLabelProp="name">
                                    <a-select-option v-for="image in imageList" :value="image.uid" :name="image.name">
                                        <img class="selector-img" :src="image.url" :alt="image.name" />
                                        <span style="margin-left: 10px">{{ image.name }}</span>
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
                <p style="margin-top: 2rem;">图像处理中，请稍后...</p>
            </div>
        </div>

        <div v-if="current == 2">
            <a-result status="success" title="图像分析成功！"
                sub-title="请在下方查看结果，或重新开始选择另一张图像。">
                <template #extra>
                    <a-button type="primary" @click="restart">重新开始</a-button>
                </template>
            </a-result>

            <a-descriptions :title="imageInfo.title + ' 处理结果'" bordered
                :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 2, xs: 1 }">
                <a-descriptions-item label="文件名">{{ imageInfo.title }}</a-descriptions-item>
                <a-descriptions-item label="文件 id">{{ imageInfo.id }}</a-descriptions-item>
                <a-descriptions-item label="原始图像">
                    <a-image width="200px" :src="imageInfo.photo"></a-image>
                </a-descriptions-item>
                <a-descriptions-item label="灰度直方图">
                    <a-image width="200px" :src="imageInfo.grayscale"></a-image>
                </a-descriptions-item>
                <a-descriptions-item label="归一化直方图">
                    <a-image width="200px" :src="imageInfo.normalization"></a-image>
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

function openImageSelector() {
    getImageList();
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

function selectImage() {
    open.value = false;
    stepNext();
    setTimeout(() => {
        requestImageInfo(selectedId.value);
    }, 3000);
}

const imageInfo = ref({});
function requestImageInfo(id) {
    axios({
        method: 'get',
        url: Server.apiUrl + '/image?id=' + id,
        accept: 'application/json',
    })
        .then((res) => {
            if (res.data.code === 200) {
                message.success("请求成功！");
                const newImageInfo = {
                    id: res.data.data[0].id,
                    title: res.data.data[0].title,
                    photo: Server.url + res.data.data[0].photo,
                    grayscale: Server.url + res.data.data[0].grayscale,
                    normalization: Server.url + res.data.data[0].normalization,
                };
                imageInfo.value = newImageInfo;
                //console.log(imageInfo.value);
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

const imageList = ref([]);
function getImageList() {
    const getLoading = message.loading('图像列表加载中...', 0);
    isLoadding.value = true;
    axios({
        method: 'get',
        url: Server.apiUrl + '/image',
        accept: 'application/json',
    })
        .then((res) => {
            if (res.data.code === 200) {
                let newlist = [];
                for (let i = 0; i < res.data.data.length; i++) {
                    newlist.push({
                        uid: res.data.data[i].id,
                        name: res.data.data[i].title,
                        status: 'done',
                        url: Server.url + res.data.data[i].photo,
                    });
                }
                imageList.value = newlist;
                getLoading(); // 关闭 loading message
                isLoadding.value = false;
                message.success("图像列表加载完成！");
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
        title: '选择图像',
    },
    {
        title: '处理图像',
    },
    {
        title: '输出结果',
    },
];
const items = steps.map(item => ({ key: item.title, title: item.title }));
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

.selector-img {
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
  