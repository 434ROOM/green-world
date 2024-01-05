<template>
    <a-layout-sider class="sider" breakpoint="lg" collapsed-width="0" :style="{ position: 'fixed' }" theme="light"
        @breakpoint="onBreakpoint">
        <a-menu v-model:selectedKeys="selectedKeys" v-model:openKeys="openKeys" mode="inline" class="menu">
            <a-sub-menu key="VideoIndex">
                <template #title>
                    <span>
                        <VideoCameraOutlined />
                        视频
                    </span>
                </template>
                <a-menu-item key="Video">
                    <router-link to="/video">交互</router-link>
                </a-menu-item>
                <a-menu-item key="VideoLib">
                    <router-link to="/video/lib">视频库</router-link>
                </a-menu-item>
            </a-sub-menu>
            <a-sub-menu key="AudioIndex">
                <template #title>
                    <span>
                        <SoundOutlined />
                        音频
                    </span>
                </template>
                <a-menu-item key="Audio">
                    <router-link to="/audio">交互</router-link>
                </a-menu-item>
                <a-menu-item key="AudioLib">
                    <router-link to="/audio/lib">音频库</router-link>
                </a-menu-item>
            </a-sub-menu>
            <a-sub-menu key="ImageIndex">
                <template #title>
                    <span>
                        <FileImageOutlined />
                        图像
                    </span>
                </template>
                <a-menu-item key="Image">
                    <router-link to="/image">交互</router-link>
                </a-menu-item>
                <a-menu-item key="ImageLib">
                    <router-link to="/image/lib">图像库</router-link>
                </a-menu-item>
            </a-sub-menu>
            <a-menu-item key="User">
                <router-link to="/user">
                    <UserOutlined />
                    用户中心
                </router-link>
            </a-menu-item>
        </a-menu>
    </a-layout-sider>
</template>

<script lang="ts">
import { ref } from 'vue';
import {
    VideoCameraOutlined,
    SoundOutlined,
    FileImageOutlined,
    UserOutlined,
} from '@ant-design/icons-vue';

const selectedKeys = ref<string[]>(['0']);
const openKeys = ref<string[]>(['0']);

const menu = [
    {
        name: 'VideoIndex',
        children: [
            {
                name: 'Video',
            },
            {
                name: 'VideoLib',
            }
        ]
    },
    {
        name: 'AudioIndex',
        children: [
            {
                name: 'Audio',
            },
            {
                name: 'AudioLib',
            }
        ]
    },
    {
        name: 'ImageIndex',
        children: [
            {
                name: 'Image',
            },
            {
                name: 'ImageLib',
            }
        ]
    },
    {
        name: 'User',
        children: [
            {
                name: 'User',
            }
        ]
    }
]


const isSmallScreen = ref(false);

export default {
    components: {
        VideoCameraOutlined,
        SoundOutlined,
        FileImageOutlined,
        UserOutlined,
    },
    mounted() {
        let pageName = this.$route.name;
        selectedKeys.value = [pageName];
        menu.forEach((item) => {
            if (item.children) {
                item.children.forEach((child) => {
                    if (child.name === pageName) {
                        openKeys.value = [item.name];
                    }
                })
            }
        })
        //console.log(selectedKeys.value);
        //console.log(openKeys.value);
    },
    methods: {
        onBreakpoint(broken: boolean) {
            this.$emit('isSmallScreen', broken);
        },
    },
    setup() {
        return {
            selectedKeys,
            openKeys,
            isSmallScreen,
        }
    }
}
</script>


<style scoped>
.sider {
    display: fixed;
    z-index: 15;
    width: 200px;
    height: calc(100vh - 64px);
    background: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)
}

.menu {
    width: 100%;
    height: 100%;
}
</style>

