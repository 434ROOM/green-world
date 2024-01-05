<template>
    <a-avatar :size="64" :src="userProfile.avatar" style="margin-bottom: 2rem;">
        {{ userProfile.username ? userProfile.username[0].toUpperCase() : 'null' }}
    </a-avatar>
    <a-button type="primary" @click="openAvatarModal">修改头像</a-button>

    <a-modal v-model:open="avatarModalVisable" title="修改头像" :footer="null">
        <a-modal v-model:open="cutVisable" title="剪裁头像" @ok="finishCut">
            <vue-cropper ref="cropper" :img="options.img" :info="true" :autoCrop="options.autoCrop"
                :autoCropWidth="options.autoCropWidth" :autoCropHeight="options.autoCropHeight" :fixedBox="options.fixedBox"
                :previewsCircle="options.previewsCircle" :realTime="realTime" style="width: 100%;min-height: 400px;">
            </vue-cropper>
        </a-modal>

        <a-upload v-model:file-list="fileList" name="avatar" list-type="picture-card" class="avatar-uploader"
            :show-upload-list="false" :before-upload="beforeUpload" :custom-request="handleUpload" @change="handleChange">
            <div v-if="imageUrl" class="img-box">
                <img :src="imageUrl" alt="avatar" />
            </div>
            <div v-else>
                <loading-outlined v-if="loading"></loading-outlined>
                <plus-outlined v-else></plus-outlined>
                <div class="ant-upload-text">上传头像</div>
            </div>
        </a-upload>
    </a-modal>
</template>
  
<script setup>
import { ref } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';
import { PlusOutlined, LoadingOutlined } from '@ant-design/icons-vue';
import 'vue-cropper/dist/index.css'
import { VueCropper } from "vue-cropper";

import JWTToken from '@/JWTToken.js';
import serverConfig from '@/serverConfig';
import EventBus from '@/EventBus';

const userProfile = ref({
    user_id: JWTToken.getUserId(),
    username: JWTToken.getUsername(),
    email: JWTToken.getEmail(),
    avatar: JWTToken.getAvatar(),
});

EventBus.on('userProfileChanged', () => {
    userProfile.value = {
        user_id: JWTToken.getUserId(),
        username: JWTToken.getUsername(),
        email: JWTToken.getEmail(),
        avatar: JWTToken.getAvatar(),
    };
});

const options = ref({
    img: "", //裁剪图片的地址
    autoCrop: true, //是否默认生成截图框
    autoCropWidth: 200, //默认生成截图框宽度
    autoCropHeight: 200, //默认生成截图框高度
    fixedBox: true, //是否固定截图框大小 不允许改变
    previewsCircle: true, //预览图是否是原圆形
    title: "修改图片",
});

const avatarModalVisable = ref(false);
const cutVisable = ref(false);
const fileList = ref([]);
const loading = ref(false);
const imageUrl = ref('');

const openAvatarModal = () => {
    avatarModalVisable.value = true;
};

const handleChange = (info) => {
    if (info.file.status === 'uploading') {
        loading.value = true;
        return;
    }
    if (info.file.status === 'done') {
        imageUrl.value = info.file.response.avatar;
        loading.value = false;
        message.success('头像上传成功');
        JWTToken.getProfile();
    }
    if (info.file.status === 'error') {
        loading.value = false;
        message.error('头像上传失败，请稍后重试');
        fileList.value = [];
        avatarModalVisable.value = false;
    }
};


const realTime = (data) => {
    console.log('Real time data: ', data);
    // 在这里可以实时获取裁剪的数据，例如裁剪框的坐标、宽高等
};

const finishCut = async () => {
    cutVisable.value = false;
    avatarModalVisable.value = false;
    EventBus.emit('finishCut');
};

function base64ToFile(base64String, fileName, mimeType) {
    // 将 base64 字符串转换为 ArrayBuffer
    const byteCharacters = atob(base64String);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: mimeType });

    // 创建一个新的 File 对象
    const file = new File([blob], fileName, { type: mimeType });
    return file;
}

const cropper = ref();
const beforeUpload = async (file) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJpgOrPng) {
        message.error('头像只能是 JPG/PNG 格式的图片');
        return false;
    }

    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
        message.error('头像大小不能超过 2MB');
        return false;
    }
    if (isJpgOrPng && isLt2M) {
        options.value.img = URL.createObjectURL(file);
        cutVisable.value = true;
        //console.log(file);
        return new Promise((resolve) => {
            EventBus.on('finishCut', async () => {
                cropper.value.getCropData((data) => {
                    const base64 = data.split(',')[1];
                    const mimeType = data.split(';')[0].split(':')[1];
                    const fileName = 'avatar.' + mimeType.split('/')[1];
                    const newFile = base64ToFile(base64, fileName, mimeType);
                    EventBus.off('finishCut');
                    resolve(newFile)
                });
            });
        });
    }
    return false;
};


function handleUpload(data) {
    let { file, onSuccess, onError, onProgress } = data;
    const formData = new FormData();
    formData.append('avatar', file);
    //console.log(file);

    axios({
        method: 'post',
        url: serverConfig.apiUrl + '/user/change-avatar',
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
            if (res.data.code === 201 || res.data.code === 200) {
                let fileInfo = {
                    avatar: serverConfig.url + res.data.data.avatar,
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

</script>

<style scoped>

.avatar-uploader>.ant-upload {
    width: 128px;
    height: 128px;
    overflow: hidden;
}

.avatar-uploader .ant-upload img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.img-box {
    width: 100%;
    height: 100%;
    overflow: hidden;
    border-radius: 8px;
}

.ant-upload-select-picture-card i {
    font-size: 32px;
    color: #999;
}

.ant-upload-select-picture-card .ant-upload-text {
    margin-top: 8px;
    color: #666;
}
</style>
  