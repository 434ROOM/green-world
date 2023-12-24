import { createApp } from 'vue';
import Antd from 'ant-design-vue';
import App from './App.vue';
import 'ant-design-vue/dist/reset.css';

import router from './router'; // 导入路由配置文件

const app = createApp(App);

app.use(Antd).use(router).mount('#app');