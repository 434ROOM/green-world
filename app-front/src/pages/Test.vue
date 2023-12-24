<template>
  <div>
    <a-button type="primary" @click="handleClick">Click me!</a-button>
    <a-modal v-model:open="modalVisible" title="Modal Title">
      <p>Content of the modal</p>
      <p>More content...</p>
    </a-modal>
  </div>
</template>

<script>
import { ref } from 'vue';
export default {
  setup() {
    // 使用 ref 创建一个响应式变量，用于控制 Modal 的显示和隐藏
    const modalVisible = ref(false);

    // 点击按钮时显示 Modal
    const handleClick = () => {
      modalVisible.value = true;
    };

    return {
      modalVisible,
      handleClick,
    };
  },
};
</script>

<style>
/* 样式可根据需要进行修改 */
</style>
