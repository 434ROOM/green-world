<template>
    <a-segmented v-model:value="switchCode" block :options="switchData" size="large" style="margin-bottom: 2rem;" />
    <div v-if="switchCode == 'profile'">
        <a-row :gutter="[16, 16]" style="margin-bottom: 2rem;">
            <a-col :span="3" style="max-width: 92px;">
                <a-avatar :size="64" :src="userProfile.avatar">
                    {{ userProfile.username ? userProfile.username[0].toUpperCase() : 'null' }}
                </a-avatar>
            </a-col>

            <a-col :xs="24" :sm="24" :md="21" :lg="21" :xl="21">
                <div class="name-area">
                    <span class="name">
                        {{ userProfile.username ? userProfile.username : 'null' }}
                    </span>
                    <span>
                        <MailOutlined />
                        {{ userProfile.email ? userProfile.email : 'null' }}
                    </span>
                </div>
            </a-col>
        </a-row>

        <a-input-group compact>
            <a-input v-model:value="newUsername" placeholder="更改用户名" style="width: 100%; max-width: 200px;" />
            <a-button type="primary" @click="changeUsername">提交</a-button>
        </a-input-group>

    </div>

    <div v-if="switchCode == 'avatar'" class="avatar-area">
        <a-avatar :size="64" :src="userProfile.avatar" style="margin-bottom: 2rem;">
            {{ userProfile.username ? userProfile.username[0].toUpperCase() : 'null' }}
        </a-avatar>
        <a-button type="primary" @click="openAvatarModal">修改头像</a-button>

        <a-modal v-model:visible="avatarModalVisable" title="修改头像" :footer="null">
            <a-upload v-model:file-list="fileList" name="avatar" list-type="picture-card" class="avatar-uploader"
                :show-upload-list="false" :before-upload="beforeUpload" :custom-request="handleUpload" @change="handleChange">
                <img v-if="imageUrl" :src="imageUrl" alt="avatar" />
                <div v-else>
                    <loading-outlined v-if="loading"></loading-outlined>
                    <plus-outlined v-else></plus-outlined>
                    <div class="ant-upload-text">Upload</div>
                </div>
            </a-upload>
        </a-modal>
    </div>

    <div v-if="switchCode == 'password'">

    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { MailOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import axios from 'axios';

import JWTToken from '@/JWTToken.js';
import serverConfig from '@/serverConfig';

const switchData = ref([
    {
        label: '个人信息',
        value: 'profile',
    },
    {
        label: '修改头像',
        value: 'avatar',
    },
    {
        label: '修改密码',
        value: 'password',
    },
]);

const switchCode = ref('profile');
const newUsername = ref('');

const userProfile = ref({
    user_id: JWTToken.getUserId(),
    username: JWTToken.getUsername(),
    email: JWTToken.getEmail(),
    avatar: JWTToken.getAvatar(),
});

function checkNewUsername() {
    let isVaild = true;
    if (newUsername.value == '') {
        message.error('用户名不能为空');
        isVaild = false;
        return isVaild;
    }
    if (newUsername.value == userProfile.value.username) {
        message.error('用户名不能与原用户名相同');
        isVaild = false;
        return isVaild;
    }
    if (newUsername.value.length > 20) {
        message.error('用户名长度不能超过 20 个字符');
        isVaild = false;
        return isVaild;
    }
    if (newUsername.value.length < 4) {
        message.error('用户名长度不能少于 4 个字符');
        isVaild = false;
        return isVaild;
    }
    if (!/^[a-zA-Z0-9_]+$/.test(newUsername.value)) {
        message.error('用户名只能包含字母、数字和下划线');
        isVaild = false;
        return isVaild;
    }
    if (newUsername.value[0] == '_') {
        message.error('用户名不能以下划线开头');
        isVaild = false;
        return isVaild;
    }
    if (newUsername.value[newUsername.value.length - 1] == '_') {
        message.error('用户名不能以下划线结尾');
        isVaild = false;
        return isVaild;
    }
    if (newUsername.value.indexOf('__') != -1) {
        message.error('用户名不能包含连续的下划线');
        isVaild = false;
        return isVaild;
    }
    return isVaild;
}

function changeUsername() {
    if (!checkNewUsername()) {
        return;
    }
    const fromData = new FormData();
    fromData.append('username', newUsername.value);

    axios.post(serverConfig.apiUrl + '/user/change-sername', fromData, {
        headers: {
            'Authorization': JWTToken.getToken(),
            "Content-Type": "multipart/form-data",
        },
    }
    ).then((res) => {
        if (res.status == 200) {
            message.success('用户名修改成功');
            JWTToken.refreshToken();
            window.location.reload();
        } else {
            message.error('用户名修改失败');
        }
    }).catch((err) => {
        message.error('用户名修改失败');
        console.log(err);
    });
}

const avatarModalVisable = ref(false);
function openAvatarModal() {
    avatarModalVisable.value = true;
}

import { PlusOutlined, LoadingOutlined } from '@ant-design/icons-vue';
import type { UploadChangeParam, UploadProps } from 'ant-design-vue';

function getBase64(img: Blob, callback: (base64Url: string) => void) {
    const reader = new FileReader();
    reader.addEventListener('load', () => callback(reader.result as string));
    reader.readAsDataURL(img);
}

const fileList = ref([]);
const loading = ref<boolean>(false);
const imageUrl = ref<string>('');

const handleChange = (info: UploadChangeParam) => {
    if (info.file.status === 'uploading') {
        loading.value = true;
        return;
    }
    if (info.file.status === 'done') {
        // Get this url from response in real world.
        getBase64(info.file.originFileObj, (base64Url: string) => {
            imageUrl.value = base64Url;
            loading.value = false;
        });
    }
    if (info.file.status === 'error') {
        loading.value = false;
        message.error('upload error');
    }
};

const beforeUpload = (file: UploadProps['fileList'][number]) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJpgOrPng) {
        message.error('头像只能是 JPG/PNG 格式的图片');
    }
    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
        message.error('头像大小不能超过 2MB');
    }
    return isJpgOrPng && isLt2M;
};

function handleUpload(data: { file: any; onSuccess: any; onError: any; onProgress: any; }) {
    let { file, onSuccess, onError, onProgress } = data;
    const formData = new FormData();
    formData.append('avatar', file);

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

</script>

<style scoped>
.name-area {
    height: 64px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.name {
    word-wrap: break-word;
    font-size: 1.5rem;
    font-weight: bold;
}

.avatar-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.avatar-uploader>.ant-upload {
    width: 128px;
    height: 128px;
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