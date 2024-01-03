<template>
    <a-button class="refresh" type="primary" :loading="isRefresh" @click="getAudioList">
        {{ isRefresh ? "Loading" : "刷新列表" }}
    </a-button>
    <div class="clearfix">
        <a-upload v-model:file-list="fileList" :custom-request="handleUpload" list-type="picture-card" :multiple="false"
            @preview="handlePreview" accept="audio/wave, audio/wav" :before-upload="beforeUpload" @change="handleChange"
            @remove="beforeDelete">
            <template #previewIcon>
                <SoundOutlined @click="handlePreview" class="play-btn" style="color: rgba(255, 255, 255, 0.8)" />
            </template>
            <div v-if="fileList.length < 8">
                <plus-outlined />
                <div style="margin-top: 8px">上传音频</div>
            </div>
        </a-upload>
        <a-modal :open="previewVisible" :title="previewTitle" :footer="null" @cancel="handleCancel">
            <audio width="100%" style="margin-top: 1rem;" :key="previewTitle" controls>
                <source :src="previewAudio">
                您的浏览器不支持 HTML5 audio 标签。
            </audio>
        </a-modal>
    </div>
</template>


<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { reactive } from 'vue';
import { createVNode } from 'vue';
import axios from 'axios';

import {
    PlusOutlined,
    SoundOutlined,
    ExclamationCircleOutlined
} from '@ant-design/icons-vue';

import {
    Upload,
    message,
    Modal
} from 'ant-design-vue';

import Server from '../serverConfig.js';

import audioIcon from '../assets/images/interacteion/icon-audio.png';

// 上传前的检查
const beforeUpload = file => {
    const isWave = file.type === 'audio/wave';
    const isWav = file.type === 'audio/wav';
    const isFormat = isWave || isWav;
    if (!isFormat) {
        message.error('音频格式不正确，请上传 .wav 或 .wave 格式的音频！');
    }
    const isLt10M = file.size / 1024 / 1024 < 10;
    if (!isLt10M) {
        message.error('音频大小不能超过 10MB！');
    }
    const isLt8 = fileList.value.length < 8;
    if (!isLt8) {
        openAudioLibFulled();
    }
    const res = isFormat && isLt10M && isLt8;
    return res || Upload.LIST_IGNORE;//不上传
}

const previewVisible = ref(false);
const previewAudio = ref('');
const previewTitle = ref('');
const fileList = ref([]);

// 关闭预览
const handleCancel = () => {
    previewVisible.value = false;
    previewTitle.value = '';
};

// 预览
const handlePreview = async file => {
    previewAudio.value = file.url;
    previewTitle.value = file.name;
    previewVisible.value = true;
};


// 上传
function handleUpload(data) {
    let { file, onSuccess, onError, onProgress } = data;
    const formData = new FormData();
    formData.append('audio', file);

    axios({
        method: 'post',
        url: Server.apiUrl + '/add-audio',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            onProgress({ percent: percentCompleted });
        },
    })
        .then((res) => {
            if (res.status === 201) {
                let fileInfo = {
                    uid: res.data.data.id,
                    name: res.data.data.title,
                    status: 'done',
                    thumbUrl: audioIcon,
                    url: Server.url + res.data.data.audio,
                };
                onSuccess(fileInfo, file);
            } else {
                throw new Error(`${res.data.code} ${res.data.msg}`);
            }
        })
        .catch((error) => {
            console.error(error.message);
            onError(error.message, file);
        });
}

// change
function handleChange(data) {
    let { file, fileList } = data;
    if (file.status === 'removed') {
        axios({
            method: 'delete',
            url: Server.apiUrl + '/audio' + '?id=' + file.uid,
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((res) => {
                if (res.data.code === 200) {
                    message.success('删除成功！');
                } else {
                    throw new Error(`${res.data.code} ${res.data.msg}`);
                }
            })
            .catch((error) => {
                message.error('删除失败，请稍后重试！');
                console.error(error.message);
                getAudioList();
            });
    }
    if (file.status === 'done') {
        const newFileInfo = reactive({
            uid: file.response.uid,
            name: file.response.name,
            status: 'done',
            thumbUrl: file.response.thumbUrl,
            url: file.response.url,
        }, {});
        //console.log(newFileInfo);
        for (let i = 0; i < fileList.length; i++) {
            if (fileList[i].uid === file.uid) {
                fileList[i] = newFileInfo;
                break;
            }
        }
        message.success('上传成功！');
        if (fileList.length >= 8) {
            openAudioLibFulled();
        }
    }
    if (file.status === 'error') {
        message.error('上传失败，请稍后重试！');
    }
}


const isRefresh = ref(false);

// 获取音频列表
function getAudioList() {
    isRefresh.value = true;
    const getLoading = message.loading('音频列表加载中...', 0);
    axios({
        method: 'get',
        url: Server.apiUrl + '/audio',
        accept: 'application/json',
    })
        .then((res) => {
            if (res.status === 200) {
                let newlist = [];
                for (let i = 0; i < res.data.data.length; i++) {
                    newlist.push({
                        uid: res.data.data[i].id,
                        name: res.data.data[i].title,
                        status: 'done',
                        thumbUrl: audioIcon,
                        url: Server.url + res.data.data[i].audio,
                    });
                }
                fileList.value = newlist;
                getLoading(); // 关闭 loading message
                isRefresh.value = false;
                message.success("音频列表加载完成！");
            } else if (res.status === 204) {
                fileList.value = [];
                getLoading(); // 关闭 loading message
                isRefresh.value = false;
                message.success("音频列表加载完成！");
            } else {
                throw new Error(res.data.code + " " + res.data.msg); // 抛出一个错误，进入到 catch 中
            }
        })
        .catch((error) => {
            console.error(error.message); // 错误处理
            getLoading(); // 关闭 loading message
            isRefresh.value = false;
            message.error("请求失败，请稍后重试！"); // 错误提示
            return false; // 返回 false 表示请求失败
        });
}

// 通知
import { notification } from 'ant-design-vue';
function openAudioLibFulled() {
    notification.warning({
        message: '音频库已满',
        description:
            '为了安全，音频库最多只能存储 8 个。如需上传新音频，请先删除旧音频。',
    });
};

// 删除前确认
const showDeleteConfirm = () => {
    return new Promise((resolve, reject) => {
        Modal.confirm({
            title: '是否确认删除？',
            icon: createVNode(ExclamationCircleOutlined),
            content: '请注意，删除后无法恢复！',
            okText: '确认',
            okType: 'danger',
            cancelText: '取消',
            onOk() {
                resolve(true);
            },
            onCancel() {
                resolve(false);
            },
        });
    });
};

async function beforeDelete() {
    const isDelete = await showDeleteConfirm();
    return isDelete;
}

// 生命周期
onMounted(() => {
    getAudioList();
    if (fileList.value.length >= 8) {
        openAudioLibFulled();
    }
});
</script>


<style scoped>
/* you can make up upload button and sample style by using stylesheets */

.ant-upload-select-picture-card i {
    font-size: 32px;
    color: #999;
}

.ant-upload-select-picture-card .ant-upload-text {
    margin-top: 8px;
    color: #666;
}

.refresh {
    margin-bottom: 1.5rem;
}
</style>