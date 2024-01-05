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
        <AvatarUpload />
    </div>

    <div v-if="switchCode == 'password'">
        <a-form :model="changePasswordFormState" name="normal_login" class="change-password-form" @submit="changePassword">

            <a-form-item name="old_password" :rules="[{ required: true, message: '请输入旧密码！' }]">
                <a-input-password v-model:value="changePasswordFormState.password" placeholder="旧密码">
                    <template #prefix>
                        <LockOutlined class="site-form-item-icon" />
                    </template>
                </a-input-password>
            </a-form-item>

            <a-form-item name="password" :rules="[{ required: true, message: '请输入新密码！' }]">
                <a-input-password v-model:value="changePasswordFormState.password" placeholder="新密码">
                    <template #prefix>
                        <LockOutlined class="site-form-item-icon" />
                    </template>
                </a-input-password>
            </a-form-item>

            <a-form-item name="confirm" :rules="[{ required: true, message: '请确认新密码！' }]">
                <a-input-password v-model:value="changePasswordFormState.confirm" placeholder="确认新密码">
                    <template #prefix>
                        <LockOutlined class="site-form-item-icon" />
                    </template>
                </a-input-password>
            </a-form-item>

            <a-form-item no-style>
                <div class="change-password-btn">
                    <a-button :disabled="registerDisabled" type="primary" html-type="submit">
                        修改密码
                    </a-button>
                </div>
            </a-form-item>
        </a-form>
    </div>
</template>

<script lang="ts" setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { reactive } from 'vue';
import { MailOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { LockOutlined } from '@ant-design/icons-vue';
import axios from 'axios';

import AvatarUpload from '@/components/AvatarUpload.vue';
import JWTToken from '@/JWTToken.js';
import serverConfig from '@/serverConfig';
import EventBus from '@/EventBus';

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

onMounted(() => {
    EventBus.on('userProfileChanged', () => {
        userProfile.value = {
            user_id: JWTToken.getUserId(),
            username: JWTToken.getUsername(),
            email: JWTToken.getEmail(),
            avatar: JWTToken.getAvatar(),
        };
    });
});

onBeforeUnmount(() => {
    EventBus.off('userProfileChanged');
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

    axios.post(serverConfig.apiUrl + '/user/change-profile', fromData, {
        headers: {
            'Authorization': 'Bearer ' + JWTToken.getAccessToken(),
            "Content-Type": "multipart/form-data",
        },
    }
    ).then((res) => {
        if (res.status == 200) {
            newUsername.value = '';
            message.success('用户名修改成功');
            JWTToken.refreshToken();
        } else {
            message.error('用户名修改失败');
        }
    }).catch((err) => {
        message.error('用户名修改失败');
        console.log(err);
    });
}

// 修改密码
interface ChangePasswordFormState {
    old_password: string;
    password: string;
    confirm: string;
}

const changePasswordFormState = reactive<ChangePasswordFormState>({
    old_password: '',
    password: '',
    confirm: '',
});

const registerDisabled = computed(() => {
    let isFinish = changePasswordFormState.old_password && changePasswordFormState.password && changePasswordFormState.confirm;
    let isSame = changePasswordFormState.password === changePasswordFormState.confirm;
    return !(isFinish && isSame);
});
function changePassword() {
    const formData = new FormData();
    formData.append('old_password', changePasswordFormState.old_password);
    formData.append('password', changePasswordFormState.password);

    // 构造axios请求，注意headers应该是配置对象的一部分
    axios.post(serverConfig.apiUrl + '/user/change-password', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
        .then((res) => {
            if (res.status === 200) { // 在axios中，响应状态码通常在res.data中，这里可能需要调整
                message.success('密码修改成功，请使用重新登录！');
                setTimeout(() => {
                    JWTToken.logout();
                }, 1000);
            } else {
                message.error(res.data.message); // 响应数据可能在res.data中
            }
        })
        .catch((err) => {
            if (err.response && err.response.data) {
                // 处理响应错误，如果服务器返回了错误信息
                if (err.response.status === 401) {
                    message.error('密码修改失败，请检查原密码是否正确！');
                } else {
                    message.error(err.response.data.msg || '密码修改失败，请稍后重试！');
                }
            }
            else {
                // 处理其他类型的错误，比如网络错误等
                console.error(err);
                message.error('密码修改失败，请检查网络连接并重试！');
            }
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

.change-password-form {
    width: 100%;
    max-width: 360px;
    margin: 0 auto;
}

.change-password-form .change-password-btn {
    display: flex;
    justify-content: center;
}
</style>