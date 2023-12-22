<template>
    <div>
        <a-steps :current="current" :items="items"></a-steps>
        <div class="steps-content">
            <div v-if="current == 0">
                <a-row>
                    <a-col :span="12" class="card">
                        <a-space direction="vertical">
                            <a-typography-title :level="5"> 还没有图像？</a-typography-title>
                            <a-button type="primary">
                                <router-link to="/image/lib">去上传</router-link>
                            </a-button>
                        </a-space>
                    </a-col>
                    <a-col :span="12" class="card">
                        <a-space direction="vertical">
                            <a-typography-title :level="5">已有图像？</a-typography-title>
                            <a-button type="primary">选一张</a-button>
                        </a-space>
                    </a-col>
                </a-row>
            </div>
        </div>
        <div class="steps-action">
            <a-button v-if="current < steps.length - 1" type="primary" @click="next">Next</a-button>
            <a-button v-if="current == steps.length - 1" type="primary" @click="message.success('Processing complete!')">
                Done
            </a-button>
            <a-button v-if="current > 0" style="margin-left: 8px" @click="prev">Previous</a-button>
        </div>
    </div>
</template>


<script lang="ts" setup>
import { ref } from 'vue';
import { message } from 'ant-design-vue';

const current = ref<number>(0);
const next = () => {
    current.value++;
};
const prev = () => {
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
        title: '结果输出',
    },
];
const items = steps.map(item => ({ key: item.title, title: item.title }));
</script>


<style scoped>
.steps-content {
    height: 60vh;
    margin-top: 3vh;
    border: 1px dashed #e9e9e9;
    border-radius: 6px;
    background-color: #fafafa;
    min-height: 200px;
    text-align: center;
    padding: 30px 50px;
}

.card{
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.steps-action {
    margin-top: 24px;
}

[data-theme='dark'] .steps-content {
    background-color: #2f2f2f;
    border: 1px dashed #404040;
}
</style>
  