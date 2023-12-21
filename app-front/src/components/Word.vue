<template>
    <div class="bg">
        <img class="text" src="../assets/images/index/text.png" alt="" draggable="false">
        <a-button ghost class="goto-btn"><router-link to="/video">Have a try
                <ArrowRightOutlined class="icon" />
            </router-link></a-button>
    </div>
</template>

<script setup>
import { ArrowRightOutlined } from '@ant-design/icons-vue';
</script>

<style scoped>
.bg {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background-image: url('../assets/images/index/lake.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    text-align: center;
    color: #fff;
    padding: 5rem 2rem;
}

.text {
    width: 100%;
    max-width: 800px;
}

.goto-btn {
    margin-top: 2rem;
}

.icon {
    margin-left: .5rem;
}

</style>
