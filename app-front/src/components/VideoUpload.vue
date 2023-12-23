<template>
    <a-button class="refresh" type="primary" :loading="isRefresh" @click="getVideoList">
        {{ isRefresh ? "Loading" : "刷新列表" }}
    </a-button>
    <div class="clearfix">
        <a-upload v-model:file-list="fileList" :custom-request="handleUpload" list-type="picture-card" :multiple="true"
            @preview="handlePreview" accept="video/mp4" :before-upload="beforeUpload" @change="handleChange">
            <div v-if="fileList.length < 8">
                <plus-outlined />
                <div style="margin-top: 8px">上传视频</div>
            </div>
        </a-upload>
        <a-modal :open="previewVisible" :title="previewTitle" :footer="null" @cancel="handleCancel">
            <video width="100%" controls style="margin-top: 1rem;">
                <source :src="previewVideo">
                您的浏览器不支持 HTML5 video 标签。
            </video>
        </a-modal>
    </div>
</template>


<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { reactive } from 'vue';
import axios from 'axios';
import { PlusOutlined } from '@ant-design/icons-vue';
import { Upload, message } from 'ant-design-vue';
import Server from '../serverConfig.js';

// 上传前的检查
const beforeUpload = file => {
    const isMp4 = file.type === 'video/mp4';
    if (!isMp4) {
        message.error('仅支持上传 mp4 格式！');
    }
    const isLt30M = file.size / 1024 / 1024 < 30;
    if (!isLt30M) {
        message.error('视频大小不能超过 30MB！');
    }
    const isLt8 = fileList.value.length < 8;
    if (!isLt8) {
        openVideoLibFulled();
    }
    const res = isMp4 && isLt30M && isLt8;
    return res || Upload.LIST_IGNORE;//不上传
}

const previewVisible = ref(false);
const previewVideo = ref('');
const previewTitle = ref('');
const fileList = ref([]);

// 关闭预览
const handleCancel = () => {
    previewVisible.value = false;
    previewTitle.value = '';
};

// 预览
const handlePreview = async file => {
    previewVideo.value = file.url;
    previewVisible.value = true;
    previewTitle.value = file.name || file.url.substring(file.url.lastIndexOf('/') + 1);
};


// 上传
function handleUpload(data) {
    let { file, onSuccess, onError, onProgress } = data;
    const formData = new FormData();
    formData.append('video_file', file);

    axios({
        method: 'post',
        url: Server.apiUrl + '/add-video',
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
            if (res.data.code === 201) {
                let fileInfo = {
                    uid: res.data.data.id,
                    name: res.data.data.title,
                    status: 'done',
                    thumbUrl: Server.url + res.data.data.cover,
                    url: Server.url + res.data.data.video_file,
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
            url: Server.apiUrl + '/video' + '?id=' + file.uid,
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
                getVideoList();
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
        for (let i = 0; i < fileList.length; i++) {
            if (fileList[i].uid === file.uid) {
                fileList[i] = newFileInfo;
                break;
            }
        }
        message.success('上传成功！');
        if (fileList.length >= 8) {
            openVideoLibFulled();
        }
    }
    if (file.status === 'error') {
        message.error('上传失败，请稍后重试！');
    }
}


const isRefresh = ref(false);

// 获取视频列表
function getVideoList() {
    isRefresh.value = true;
    const getLoading = message.loading('视频列表加载中...', 0);
    axios({
        method: 'get',
        url: Server.apiUrl + '/video',
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
                        thumbUrl: Server.url + res.data.data[i].cover,
                        url: Server.url + res.data.data[i].video_file,
                    });
                }
                fileList.value = newlist;
                getLoading(); // 关闭 loading message
                isRefresh.value = false;
                message.success("视频列表加载完成！");
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
function openVideoLibFulled() {
    notification.warning({
        message: '视频库已满',
        description:
            '为了安全，视频库最多只能存储 8 个。如需上传新视频，请先删除旧视频。',
    });
};


// 生命周期
onMounted(() => {
    getVideoList();
    if (fileList.value.length >= 8) {
        openVideoLibFulled();
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