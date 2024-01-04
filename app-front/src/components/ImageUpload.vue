<template>
    <a-button class="refresh" type="primary" :loading="isRefresh" @click="getImageList">
        {{ isRefresh ? "Loading" : "刷新列表" }}
    </a-button>
    <div class="clearfix">
        <a-upload v-model:file-list="fileList" :custom-request="handleUpload" list-type="picture-card" :multiple="false"
            @preview="handlePreview" accept="image/png, image/jpeg" :before-upload="beforeUpload" @change="handleChange"
            @remove="beforeDelete">
            <div v-if="fileList.length < 8">
                <plus-outlined />
                <div style="margin-top: 8px">上传图像</div>
            </div>
        </a-upload>
        <a-modal :open="previewVisible" :title="previewTitle" :footer="null" @cancel="handleCancel">
            <img alt="preview" style="width: 100%" :src="previewImage" />
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
    ExclamationCircleOutlined
} from '@ant-design/icons-vue';

import {
    Upload,
    message,
    Modal
} from 'ant-design-vue';

import Server from '../serverConfig.js';
import JWTToken from '@/JWTToken';

// 图像上传前的检查
const beforeUpload = file => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJpgOrPng) {
        message.error('仅支持上传 png、jpeg、jpg 格式！');
    }
    const isLt3M = file.size / 1024 / 1024 < 3;
    if (!isLt3M) {
        message.error('图像大小不能超过 3MB！');
    }
    const isLt8 = fileList.value.length < 8;
    if (!isLt8) {
        openImageLibFulled();
    }
    const res = isJpgOrPng && isLt3M && isLt8;
    return res || Upload.LIST_IGNORE;//不上传
}

// 图像base64编码
function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

const previewVisible = ref(false);
const previewImage = ref('');
const previewTitle = ref('');
const fileList = ref([]);

// 关闭预览
const handleCancel = () => {
    previewVisible.value = false;
    previewTitle.value = '';
};

// 预览
const handlePreview = async file => {
    if (!file.url && !file.preview) {
        file.preview = await getBase64(file.originFileObj);
    }
    previewImage.value = file.url || file.preview;
    previewVisible.value = true;
    previewTitle.value = file.name || file.url.substring(file.url.lastIndexOf('/') + 1);
};


// 上传
function handleUpload(data) {
    let { file, onSuccess, onError, onProgress } = data;
    const formData = new FormData();
    formData.append('photo', file);

    axios({
        method: 'post',
        url: Server.apiUrl + '/add-image',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: 'Bearer ' + JWTToken.getAccessToken(),
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
                    url: Server.url + res.data.data.photo,
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
            url: Server.apiUrl + '/image' + '?id=' + file.uid,
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + JWTToken.getAccessToken(),
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
                getImageList();
            });
    }
    if (file.status === 'done') {
        const newFileInfo = reactive({
            uid: file.response.uid,
            name: file.response.name,
            status: 'done',
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
            openImageLibFulled();
        }
    }
    if (file.status === 'error') {
        message.error('上传失败，请稍后重试！');
    }
}


const isRefresh = ref(false);

// 获取图像列表
function getImageList() {
    isRefresh.value = true;
    const getLoading = message.loading('图像列表加载中...', 0);
    axios({
        method: 'get',
        url: Server.apiUrl + '/image',
        headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + JWTToken.getAccessToken(),
        },
    })
        .then((res) => {
            if (res.status === 200) {
                let newlist = [];
                for (let i = 0; i < res.data.data.length; i++) {
                    newlist.push({
                        uid: res.data.data[i].id,
                        name: res.data.data[i].title,
                        status: 'done',
                        url: Server.url + res.data.data[i].photo,
                    });
                }
                fileList.value = newlist;
                getLoading(); // 关闭 loading message
                isRefresh.value = false;
                message.success("图像列表加载完成！");
            } else if (res.status === 204) {
                fileList.value = [];
                getLoading(); // 关闭 loading message
                isRefresh.value = false;
                message.success("图像列表加载完成！");
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
function openImageLibFulled() {
    notification.warning({
        message: '图像库已满',
        description:
            '为了安全，图像库最多只能存储 8 张图像。如需上传新图像，请先删除旧图像。',
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
    getImageList();
    if (fileList.value.length >= 8) {
        openImageLibFulled();
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
}</style>